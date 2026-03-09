# SPDX-License-Identifier: GNU GPL v3
"""
Compute AC response metrics
"""

import re
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from sgtlib.modules import ProgressUpdate, plot_to_opencv, ProgressData
from scipy.sparse.linalg import spsolve
from scipy.sparse import diags, csc_array
from matplotlib.collections import LineCollection

from ..utils.config_loader import load_rgt_configs, initialize_list_data

ALLOWED_GRAPH_FILE_EXTENSIONS = ['*.csv']
class ResponseAnalyzer(ProgressUpdate):

    def __init__(self, config_file: str = ""):
        """"""
        super(ResponseAnalyzer, self).__init__()
        self._configs: dict = load_rgt_configs(config_file)
        self._list_data: dict = initialize_list_data()
        self._network_img: None | np.ndarray = None
        self._save_path: str = ""
        self._props: list = []

    @property
    def network_img(self) -> None | np.ndarray:
        return self._network_img

    @property
    def configs(self) -> dict:
        return self._configs

    @configs.setter
    def configs(self, configs) -> None:
        self._configs = configs

    @property
    def list_data(self) -> dict:
        return self._list_data

    @list_data.setter
    def list_data(self, list_params) -> None:
        self._list_data = list_params

    @property
    def props(self) -> list:
        return self._props

    @property
    def vertices_uploaded(self) -> bool:
        """Check if the vertex coordinates were uploaded"""
        is_uploaded = True if self.list_data["vertex_coordinates"]["value"] == 1 else False
        return is_uploaded

    @property
    def edges_uploaded(self) -> bool:
        """Check if the edge list was uploaded"""
        is_uploaded = True if self.list_data["edge_list"]["value"] == 1 else False
        return is_uploaded

    @property
    def verify_uploaded_data(self) -> str | None:
        """Verify if any of the list data item has errors."""
        list_data = self.list_data
        lst_errors = ""
        for key, item in list_data.items():
            if key == "calculated_vertex_potentials" or key == "calculated_edge_currents":
                continue

            if item["value"] == -1:
                lst_errors += f"{item['text']} has errors. Please re-upload the data!"

            if key == "edge_list" and item["data"] is None:
                lst_errors += f"{item['text']} is missing. Please upload it via a CSV file!"

            if key == "vertex_coordinates" and item["data"] is None:
                lst_errors += f"{item['text']} is missing. Please upload it via a CSV file!"

        if lst_errors == "":
            return None
        return lst_errors

    def reset(self):
        """Reset all properties"""
        self._props = []
        self.list_data: dict = initialize_list_data()

    def copy_rgt_obj(self, other):
        """Copy attributes from another ResponseAnalyzer object"""
        try:
            self._network_img = other.network_img
            self.list_data["calculated_vertex_potentials"]["data"] = other.list_data["calculated_vertex_potentials"]["data"]
            self.list_data["calculated_vertex_potentials"]["value"] = other.list_data["calculated_vertex_potentials"]["value"]
            self.list_data["calculated_edge_currents"]["data"] = other.list_data["calculated_edge_currents"]["data"]
            self.list_data["calculated_edge_currents"]["value"] = other.list_data["calculated_edge_currents"]["value"]
        except AttributeError:
            return

    def get_filenames(self):
        """
        Splits the image path into file name and image directory.

        Returns:
            filename (str): image file name., output_dir (str): image directory path.
        """
        if self._save_path == "":
            return None, None

        output_dir, filename = os.path.split(self._save_path)
        for ext in ALLOWED_GRAPH_FILE_EXTENSIONS:
            ext = ext.replace('*', '')
            pattern = re.escape(ext) + r'$'
            filename = re.sub(pattern, '', filename)
        return filename, output_dir

    def get_parameter_value(self, key: str):
        """Returns the value of a parameter from the RGT configuration"""
        opt_rgt = self.configs
        coefficient = opt_rgt[key]["value"]
        multiplier = opt_rgt[key]["multiplier"]
        # print(f"{key}: {coefficient} * 10^{multiplier} = {coefficient * 10 ** multiplier}")
        return coefficient * 10 ** multiplier

    def get_response_direction(self) -> str | None:
        opt_rgt = self.configs
        res_dir = None  # Default direction

        for i in range(len(opt_rgt["potential_direction"]["items"])):
            if int(opt_rgt["potential_direction"]["items"][i]["value"]) == 1:
                res_dir = opt_rgt["potential_direction"]["items"][i]["id"]
        return res_dir

    def init_list_data(self):
        """Compute the list parameters for the response analyzer (if they were not uploaded by the user)"""
        opt_rgt = self.configs
        list_data = self.list_data

        edge_list = list_data["edge_list"]["data"]
        vert_pos = list_data["vertex_coordinates"]["data"]
        resistivity = self.get_parameter_value("resistivity")
        capacitance = self.get_parameter_value("capacitance")
        inductance = self.get_parameter_value("inductance")
        leak_resistivity = self.get_parameter_value("leak_resistivity")

        if list_data["resistivity_list"]["value"] == 0 or list_data["resistivity_list"]["data"] is None:
            # The array of resistance for each EDGE
            list_data["resistivity_list"]["data"] = resistivity * np.ones(len(edge_list))

        if list_data["inductance_list"]["value"] == 0 or list_data["inductance_list"]["data"] is None:
            # The array of inductance for each EDGE
            list_data["inductance_list"]["data"] = inductance * np.ones(len(edge_list))

        if list_data["given_potential_list"]["value"] == 0 or list_data["given_potential_list"]["data"] is None:
            given_potential_fraction = float(opt_rgt["potential_fraction"]["value"])
            num_vertices = len(vert_pos)
            num_selected = int(given_potential_fraction * num_vertices)
            list_data["given_potential_list"]["data"] = np.zeros(int(2 * num_selected))

        num_vertices = len(vert_pos)
        num_selected = len(list_data["given_potential_list"]["data"])
        vertex_list = np.ones(num_vertices - num_selected)
        if list_data["capacitance_list"]["value"] == 0 or list_data["capacitance_list"]["data"] is None:
            # The array of capacitance for each NODE that is NOT given an applied potential. nodes are taken to be capacitors connected to a grounded potential (0).
            list_data["capacitance_list"]["data"] = capacitance * vertex_list

        if list_data["leak_resistivity_list"]["value"] == 0 or list_data["leak_resistivity_list"]["data"] is None:
            # The array of resistance between each NODE that is NOT given an applied potential and the ground, a "leakage" resistance.
            list_data["leak_resistivity_list"]["data"] = leak_resistivity * vertex_list

    def run_analyzer(self) -> None:
        """Executes functions that will compute AC Response and draw the response graph"""

        if self.abort:
            self.update_status([-1, "Problem encountered while running Response Analyzer.."])
            return

        try:
            # 1. Compute AC Response
            vertex_potentials, edge_currents = self.compute_ac_response()
            self.list_data["calculated_vertex_potentials"]["data"] = vertex_potentials
            self.list_data["calculated_vertex_potentials"]["value"] = 1
            self.list_data["calculated_edge_currents"]["data"] = edge_currents
            self.list_data["calculated_edge_currents"]["value"] = 1
        except IndexError:
            self.update_status([-1, "One or more vertex positions are out of range! Please re-upload Vertex List."])
            self.abort = True
            return

        # 2. Draw Response Graph
        plt_fig = self.plot_electrical_response()
        self.update_status(ProgressData(percent=80, sender="RGT", message=f"Saving graph plot..."))
        self._network_img = plot_to_opencv(plt_fig)

    def compute_ac_response(self, silent: bool = False) -> tuple[None, None] | tuple[np.ndarray, np.ndarray]:
        """
        From my testing on square-lattice networks, this method has the time complexity of O(n^~1.4)

        Time complexity might increase significantly in networks with higher average node degree

        :return: potential_response (as a numpy array), current_response (as a numpy array)
        """

        def incidence_matrix():
            """
            Makes an incidence matrix from a list of edges in O(n) time

            :returns: the incidence matrix of the network, where rows are directed edges and columns are vertices
            """

            # We first initialize lists, to which we will append the row, column, and value of the non-zero elements that will fill our sparse incidence array
            c_rows = []
            c_cols = []
            c_vals = []

            # Appending non-zero entries and their row/col data for each edge in the list. Edges are considered directed (+1/-1), but the direction does not matter
            edge_list = list_data["edge_list"]["data"]
            num_edges = len(edge_list)
            num_vertices = len(list_data["vertex_coordinates"]["data"])
            for idx in range(len(edge_list)):
                c_rows.append(idx)
                c_cols.append(int(edge_list[idx, 0]))
                c_vals.append(-1)
                c_rows.append(idx)
                c_cols.append(int(edge_list[idx, 1]))
                c_vals.append(1)
                # It is faster to append each element/coord to a list and then make a sparse array than it is to make a sparse array and then update each element

            incidence_mat = csc_array((c_vals, (c_rows, c_cols)), shape=(num_edges, num_vertices), dtype="complex")
            return incidence_mat

        def make_potential() -> tuple[np.ndarray, np.ndarray]:
            """
            Generate an externally imposed potential field for the system.

            This function constructs a *top-down* potential configuration, where a
            prescribed potential is applied across the system from the top boundary
            to the bottom boundary. Adjusting this function allows you to impose
            different boundary conditions or potential patterns on the same physical
            system, enabling various types of experiments or simulations.

            Returns:
                tuple[np.ndarray, np.ndarray]:
                    - ua_list: Array of potential values applied to boundary nodes.
                    - va_list: Array of node indices corresponding to the applied potentials.
            """
            opt_rgt = self.configs
            vert_pos = list_data["vertex_coordinates"]["data"]
            given_potential_magnitude = float(opt_rgt["potential_magnitude"]["value"])
            potential_direction = self.get_response_direction()

            # Ultimately this is what gets passed on; the other code in this block just makes this a top-bottom potential
            given_potential_list = list_data["given_potential_list"]["data"]
            vertex_list = np.zeros_like(given_potential_list, dtype=int)
            num_selected = int(len(given_potential_list) / 2)

            if potential_direction == "LR" or potential_direction == "RL":
                # Sort vertices by x-position (Left-Right or Right-Left)
                sorted_vertices = sorted(enumerate(vert_pos), key=lambda v: v[1][0])  # Sort by x-coordinate
                top_vertices = []
                bottom_vertices = []
                left_vertices = sorted_vertices[:num_selected]  # Lowest x-values
                right_vertices = sorted_vertices[-num_selected:]  # Highest x-values
            else:
                # Sort vertices by y-position (Top-Bottom or Bottom-Top)
                sorted_vertices = sorted(enumerate(vert_pos), key=lambda x_pos: x_pos[-1][-1])  # Sort by y-coordinate
                top_vertices = sorted_vertices[-num_selected:]                                  # Top f% (highest y-values)
                bottom_vertices = sorted_vertices[:num_selected]                                # Bottom f% (lowest y-values)
                left_vertices = []
                right_vertices = []

            # Select the potential direction: 'top-down' or 'bottom-up' or 'left-right' or 'right-left'
            if potential_direction == "LR":
                pos_list = [idx for idx, _ in left_vertices]
                neg_list = [idx for idx, _ in right_vertices]
            elif potential_direction == "RL":
                pos_list = [idx for idx, _ in right_vertices]
                neg_list = [idx for idx, _ in left_vertices]
            elif potential_direction == "BT":
                pos_list = [idx for idx, _ in bottom_vertices]
                neg_list = [idx for idx, _ in top_vertices]
            else:
                # Top-Bottom
                pos_list = [idx for idx, _ in top_vertices]
                neg_list = [idx for idx, _ in bottom_vertices]

            # Assign potentials: +V to top
            for idx in range(len(pos_list)):
                given_potential_list[idx] = given_potential_magnitude
                vertex_list[idx] = pos_list[idx]

            # Assign potentials: -V to bottom
            for idx in range(len(neg_list)):
                given_potential_list[len(pos_list) + idx] = -given_potential_magnitude
                vertex_list[len(pos_list) + idx] = neg_list[idx]

            # vertex_list = np.array(vertex_list, dtype=int) # numpy array of vertices that have a forced potential casting to int in case given as float
            return given_potential_list, vertex_list

        self.update_status(ProgressData(percent=1, sender="RGT", message=f"Computing AC response...")) if not silent else None
        if self.list_data["vertex_coordinates"]["data"] is None:
            self.update_status(ProgressData(type="error", sender="RGT", message=f"Vertex positions are missing! Please upload them via a CSV file.")) if not silent else None
            return None, None
        if self.list_data["edge_list"]["data"] is None:
            self.update_status(ProgressData(type="error", sender="RGT", message=f"Edge list is missing! Please upload them via a CSV file.")) if not silent else None
            return None, None

        # Initialize response parameters and parameter lists
        self.update_status(ProgressData(percent=10, sender="RGT", message=f"Initializing response parameters...")) if not silent else None
        self.init_list_data()
        list_data = self.list_data
        cap_list = list_data["capacitance_list"]["data"]
        leak_res_list = list_data["leak_resistivity_list"]["data"]
        res_list = list_data["resistivity_list"]["data"]
        ind_list = list_data["inductance_list"]["data"]

        # Apply imposing potentials by direction
        self.update_status(ProgressData(percent=5, sender="RGT", message=f"Imposing response potential...")) if not silent else None
        c_mat = incidence_matrix()                          # The incidence matrix of the network, where rows are directed edges and columns are vertices
        if list_data["given_potential_list"]["value"] == 1 and list_data["vertex_list"]["data"] is not None:
            ua_list = list_data["given_potential_list"]["data"]
            va_list = np.array(list_data["vertex_list"]["data"], dtype=int)
        else:
            ua_list, va_list = make_potential()             # ua_list: array applied potentials; va_list: array of nodes with the corresponding applied potential

        given_potential_frequency = self.get_parameter_value("potential_frequency")
        omega = given_potential_frequency                   # The angular frequency of applied alternating potential
        vertices_count = c_mat[0].shape[0]                  # Number of vertices in the graph
        va_vertices_count = int(len(va_list))               # number of vertices in va_list
        vb_vertices_count = int(vertices_count - va_vertices_count)  # number of vertices in vb_list

        # Compute admittance, dynamical and auxiliary matrices
        self.update_status(ProgressData(percent=15, sender="RGT", message=f"Computing admittance, dynamical and auxiliary matrices...")) if not silent else None
        admittance_mat = diags(1 / (res_list + 1j * omega * ind_list))  # diags(1/(rho+1j*omega*inductance)*np.ones(len(edges))) #Y=(R+iwL)^-1, admittance matrix
        c_mat_transposed = c_mat.T                          # transpose of incidence matrix
        dynamical_mat = c_mat_transposed @ admittance_mat @ c_mat  # sparse version of the dynamical matrix

        auxiliary_mat = np.zeros(vertices_count)            # auxiliary array where the value stored at an index is 1 if that index is in va_list
        for vert in va_list:
            auxiliary_mat[vert] = 1
        vb_list = []
        for i in range(vertices_count):  # constructing vb_list in O(n) time
            if auxiliary_mat[i] == 0:
                vb_list.append(i)

        aux_a_index_list = np.zeros(vertices_count)
        for i in range(len(va_list)):
            aux_a_index_list[va_list[i]] = i

        aux_b_index_list = np.zeros(vertices_count)
        for i in range(len(vb_list)):
            aux_b_index_list[vb_list[i]] = i

        dynamical_mat_coo = dynamical_mat.tocoo()
        dynamical_mat_as_list = np.column_stack((dynamical_mat_coo.row, dynamical_mat_coo.col, dynamical_mat_coo.data))

        aa_rows = []
        aa_cols = []
        aa_vals = []

        bb_rows = []
        bb_cols = []
        bb_vals = []

        ba_rows = []
        ba_cols = []
        ba_vals = []

        for elem in dynamical_mat_as_list:
            x = int(np.real(elem[0]))
            y = int(np.real(elem[1]))
            val = elem[2]

            if auxiliary_mat[x] == 1:
                if auxiliary_mat[y] == 1:  # Daa
                    sp_x = int(aux_a_index_list[x])
                    sp_y = int(aux_a_index_list[y])
                    aa_rows.append(sp_x)
                    aa_cols.append(sp_y)
                    aa_vals.append(val)
            else:
                if auxiliary_mat[y] == 0:  # Dbb
                    sp_x = int(aux_b_index_list[x])
                    sp_y = int(aux_b_index_list[y])
                    bb_rows.append(sp_x)
                    bb_cols.append(sp_y)
                    bb_vals.append(val)
                else:  # Dba
                    sp_x = int(aux_b_index_list[x])
                    sp_y = int(aux_a_index_list[y])
                    ba_rows.append(sp_x)
                    ba_cols.append(sp_y)
                    ba_vals.append(val)

        # Creating the sub-matrices for the Dynamical matrix, dynamical_aa, dynamical_bb, dynamical_ba
        # dynamical_aa = csc_array((aa_vals, (aa_rows, aa_cols)), shape=(va_vertices_count, va_vertices_count), dtype="complex")
        dynamical_ba = csc_array((ba_vals, (ba_rows, ba_cols)), shape=(vb_vertices_count, va_vertices_count), dtype="complex")
        dynamical_bb = csc_array((bb_vals, (bb_rows, bb_cols)), shape=(vb_vertices_count, vb_vertices_count), dtype="complex")

        self.update_status(ProgressData(percent=50, sender="RGT", message=f"Solving response equation...")) if not silent else None
        # Need to solve the equation -Dba ua = (Dbb - alpha I) ub
        # LHS = p_mat, RHS = q_mat.ub
        # calculating p_mat and q_mat:
        p_mat = - dynamical_ba @ ua_list
        q_mat = dynamical_bb - diags(1j * omega * cap_list) - diags(1 / leak_res_list)

        # solving for u_b
        ub_list = spsolve(q_mat, p_mat)

        self.update_status(ProgressData(percent=75, sender="RGT", message=f"Computing potential response...")) if not silent else None
        # calculating potential response
        potential_response = np.zeros(vertices_count, dtype="complex")

        # splicing the 'a' and 'b' components of the response back into a single list
        for i in range(len(va_list)):
            potential_response[va_list[i]] = ua_list[i]

        for i in range(len(vb_list)):
            potential_response[vb_list[i]] = ub_list[i]

        self.update_status(ProgressData(percent=85, sender="RGT", message=f"Computing current response...")) if not silent else None
        # calculating current response
        current_response = admittance_mat @ c_mat @ potential_response
        return potential_response, current_response

    def plot_electrical_response(self, graph_type: str = "all", show_current_phase: bool = None, vertex_marker_size: float = None, edge_line_width: float = None, show_color_wheel: bool = None, phase_labels: dict = None) -> None | plt.Figure:
        """
        Draws the response graph of the network.
        """

        if self.list_data["calculated_vertex_potentials"]["data"] is None or self.list_data["calculated_edge_currents"]["data"] is None:
            self.update_status(ProgressData(type="error", sender="RGT", message=f"Response data is missing! Please run the compute_response() method first."))
            return None

        def complex_to_rgb(phases, mags):
            """Convert complex numbers to colors (HSV where H=phase, S=1, V=normalized magnitude)."""
            h_mat = phases / (2 * np.pi)
            s_mat = mags
            v_mat = np.ones_like(h_mat)
            hsv = np.stack([h_mat, s_mat, v_mat], axis=-1)
            return mcolors.hsv_to_rgb(hsv)

        def plot_vertices(marker_size: float = 30):
            """Plot graph vertices only."""
            # Normalize magnitudes for vertices
            pot_mags = np.abs(potential_resp)
            pot_mags_normalized = (pot_mags - pot_mags.min()) / (pot_mags.max() - pot_mags.min() + 1e-10)
            pot_phases = np.angle(potential_resp) % (2 * np.pi)

            # pot_mags_normalized
            vertex_colors = complex_to_rgb(pot_phases, np.array([x for x in pot_mags_normalized]))

            # Plot vertices
            ax.scatter(vert_pos[:, 0], vert_pos[:, 1], c=vertex_colors, s=marker_size * pot_mags_normalized, edgecolors='none', zorder=3)

        def plot_edges(edge_lw: float = 3, use_edge_colors: bool = True, normalize_colors: bool = False):
            """Plot graph edges only."""
            # Normalize magnitudes for edges
            cur_mags = np.abs(current_resp)
            cur_mags_normalized = (cur_mags - cur_mags.min()) / (cur_mags.max() - cur_mags.min() + 1e-10)
            cur_phases = np.angle(current_resp) % (2 * np.pi)

            # cur_mags_normalized
            if normalize_colors:
                edge_colors = complex_to_rgb(cur_phases, np.array([1 for _ in cur_mags_normalized]))
            else:
                edge_colors = complex_to_rgb(np.mod(2 * cur_phases, 2 * np.pi), np.array([x for x in cur_mags_normalized]))

            # Plot edges
            edge_segments = np.array([[vert_pos[int(i)], vert_pos[int(j)]] for i, j in edge_list])
            if use_edge_colors:
                edge_collection = LineCollection(edge_segments, colors=edge_colors, linewidths=edge_lw * cur_mags_normalized)
            else:
                edge_collection = LineCollection(edge_segments, colors="0", linewidths=edge_lw * cur_mags_normalized)
            ax.add_collection(edge_collection)

        def plot_color_wheel(phase_angle_labels: dict = None):
            """Plot color wheel."""
            # Create the color-wheel legend
            ax_color = fig.add_axes((0.75, 0.15, 0.15, 0.15), projection='polar')  # this vector is x-position, y-position, width, height of color-wheel

            # Create the color-wheel using bars instead of fill_between
            n_angles = 360
            theta = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)
            width = 2 * np.pi / n_angles
            radii = np.ones(n_angles)

            # Create the HSV colors for the wheel
            h = theta / (2 * np.pi)
            s = np.ones_like(h)
            v = np.ones_like(h)
            hsv = np.stack([h, s, v], axis=-1)
            colors = mcolors.hsv_to_rgb(hsv)

            # Plot the color wheel using bar plot
            ax_color.bar(theta, radii, width=width, bottom=0, color=colors) # uncomment to show color-wheel

            # Add magnitude indicator (radius)
            ax_color.plot([0, 0], [0, 1], 'k-', lw=1)  # magnitude indicator
            ax_color.text(0, 1.1, '|z|', ha='center', va='center')

            # Add the phase-angle labels
            if phase_angle_labels is None:
                phase_angle_labels = {
                    0: '0',
                    np.pi/2: r'$\pi/2$',
                    np.pi: r'$\pi$',
                    3*np.pi/2: r'$3\pi/2$'
                }

            for angle, label in phase_angle_labels.items():
                ax_color.text(angle, 1.3, label, ha='center', va='center')

            ax_color.set_xticks([])
            ax_color.set_yticks([])
            ax_color.set_theta_direction(-1)
            ax_color.set_theta_offset(np.pi / 2)
            ax_color.set_frame_on(False)

        self.update_status(ProgressData(percent=1, sender="RGT", message=f"Generating response graph..."))
        # Retrieve computed response data (should be numpy arrays)
        vert_pos = self.list_data["vertex_coordinates"]["data"]
        edge_list = self.list_data["edge_list"]["data"]
        potential_resp = self.list_data["calculated_vertex_potentials"]["data"]
        current_resp = self.list_data["calculated_edge_currents"]["data"]

        self.update_status(ProgressData(percent=5, sender="RGT", message=f"Fetching parameters..."))
        # Create a figure and an axis
        if graph_type == "all":
            fig = plt.Figure(figsize=(16.4 / 2, 10.7 / 2)) # last ordered pair is aspect ratio
            ax = fig.add_axes((0, 0, 1, 1))  # span the whole figure
            mk_size = 10 if vertex_marker_size is None else vertex_marker_size
            lw = 5 if edge_line_width is None else edge_line_width
            color_phases = False if show_current_phase is None else show_current_phase

            self.update_status(ProgressData(percent=10, sender="RGT", message=f"Plotting graph vertices..."))
            plot_vertices(marker_size=mk_size)

            self.update_status(ProgressData(percent=40, sender="RGT", message=f"Plotting graph edges..."))
            plot_edges(edge_lw=lw, use_edge_colors=color_phases, normalize_colors=True)
        else:
            fig = plt.Figure(figsize=(9, 9))
            ax = fig.add_axes((0, 0, 1, 1))  # span the whole figure
            if graph_type == "vertices":
                self.update_status(ProgressData(percent=10, sender="RGT", message=f"Plotting graph vertices..."))
                mk_size = 30 if vertex_marker_size is None else vertex_marker_size
                plot_vertices(marker_size=mk_size)
            elif graph_type == "edges":
                self.update_status(ProgressData(percent=10, sender="RGT", message=f"Plotting graph edges..."))
                lw = 3 if edge_line_width is None else edge_line_width
                color_phases = True if show_current_phase is None else show_current_phase
                plot_edges(edge_lw=lw, use_edge_colors=color_phases)

        if show_color_wheel:
            self.update_status(ProgressData(percent=60, sender="RGT", message=f"Plotting color wheel..."))
            plot_color_wheel(phase_labels)

        # Determine plot ranges
        x_min, x_max = vert_pos[:, 0].min(), vert_pos[:, 0].max()
        y_min, y_max = vert_pos[:, 1].min(), vert_pos[:, 1].max()
        x_pad = (x_max - x_min) * 0.1
        y_pad = (y_max - y_min) * 0.1
        ax.set_xlim(x_min - x_pad, x_max + x_pad)
        ax.set_ylim(y_min - y_pad, y_max + y_pad)
        #ax.set_axis_off()

        # fig.tight_layout()
        return fig

    def plot_mechanical_response(self):
        """"""
        # Setup the 2D figure
        fig, ax = plt.subplots(figsize=(10, 10))

        # --- VERTICES ---
        # Plot all original vertices as background
        ax.scatter(original_verts[:, 0], original_verts[:, 1],
                   color='black', s=10, alpha=0.3, zorder=1, label='All Vertices (Background)')

        # Plot active unpinned vertices darker
        x_unp = unpinned_verts[:, 0]
        y_unp = unpinned_verts[:, 1]
        ax.scatter(x_unp, y_unp, color='black', s=15, alpha=0.9, zorder=4)

        # --- EDGES (TENSION VISUALIZATION) ---
        segments = unpinned_verts[unpinned_edges]

        tol = 1e-8
        zero_mask = np.abs(active_tensions) < tol
        nonzero_mask = ~zero_mask

        # Add zero-tension edges
        if np.any(zero_mask):
            lc_zero = LineCollection(segments[zero_mask], colors='gray',
                                     linewidths=0.5, linestyles='dashed', alpha=0.5, zorder=2)
            ax.add_collection(lc_zero)

        # Add non-zero-tension edges
        if np.any(nonzero_mask):
            max_t = np.max(np.abs(active_tensions[nonzero_mask]))
            normalized_tensions = np.abs(active_tensions[nonzero_mask]) / (max_t + 1e-12)
            dynamic_linewidths = 0.5 + (4.0 * normalized_tensions)

            lc_nonzero = LineCollection(segments[nonzero_mask], colors='black',
                                        linewidths=dynamic_linewidths, alpha=0.8, zorder=3)
            ax.add_collection(lc_nonzero)

        # --- DISPLACEMENT ARROWS ---
        # Reshape to 2D
        disp_2d = all_displacements.reshape(-1, 2)
        u_vec, v_vec = disp_2d[:, 0], disp_2d[:, 1]

        disp_magnitudes = np.linalg.norm(disp_2d, axis=1)

        cmap = plt.get_cmap('turbo')
        norm = mcolors.Normalize(vmin=disp_magnitudes.min(), vmax=disp_magnitudes.max())
        arrow_colors = cmap(norm(disp_magnitudes))

        moved_mask = disp_magnitudes > 1e-10

        if np.any(moved_mask):
            # Auto-scaling arrows to sensible dimensions for readibility
            # Note: angles='xy' ensures vectors correctly map to graph geometry
            ax.quiver(x_unp[moved_mask], y_unp[moved_mask],
                      u_vec[moved_mask], v_vec[moved_mask],
                      color=arrow_colors[moved_mask], angles='xy', zorder=5)

        # --- COLORBAR ---
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, shrink=0.5, pad=0.05)
        cbar.set_label('Displacement Magnitude')

        # --- AESTHETICS & SCALING ---
        ax.set_title("")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_aspect('equal', adjustable='box')  # Keeps geometry undistorted

        buffer = 0.1
        x_range = original_verts[:, 0].max() - original_verts[:, 0].min()
        y_range = original_verts[:, 1].max() - original_verts[:, 1].min()

        ax.set_xlim(original_verts[:, 0].min() - buffer * x_range, original_verts[:, 0].max() + buffer * x_range)
        ax.set_ylim(original_verts[:, 1].min() - buffer * y_range, original_verts[:, 1].max() + buffer * y_range)

        plt.tight_layout()
        plt.show()

    def save_results_to_file(self) -> bool:
        """Save computed response data to a file."""
        if self.list_data["calculated_vertex_potentials"]["data"] is None or self.list_data["calculated_edge_currents"]["data"] is None:
            return False

        filename, out_dir = self.get_filenames()
        if filename is None:
            return False

        edges_filename = filename + "_EdgeCurrents.csv"
        nodes_filename = filename + "_VertexPotentials.csv"
        edges_file = os.path.join(out_dir, edges_filename)
        nodes_file = os.path.join(out_dir, nodes_filename)

        # Export the DataFrame to a CSV file without header and index
        df_pot = pd.DataFrame(self.list_data["calculated_vertex_potentials"]["data"])
        df_pot.to_csv(str(nodes_file), header=False, index=False)

        # Export the DataFrame to a CSV file without header and index
        df_curr = pd.DataFrame(self.list_data["calculated_edge_currents"]["data"])
        df_curr.to_csv(str(edges_file), header=False, index=False)
        return True