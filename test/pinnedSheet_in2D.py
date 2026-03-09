#=================================================================================
# 1 - imports
#=================================================================================

import numpy as np
from scipy.sparse import diags, csr_matrix
from scipy.sparse.linalg import spsolve, lsqr, eigsh
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import pandas as pd
import matplotlib.colors as mcolors

#=================================================================================
# 2 - functions
#=================================================================================

def generate_disordered_triangular_lattice(nx=10, ny=10, spacing=1.0, disorder_strength=0.2):
    """
    Generates a disordered 2D triangular lattice.
    
    Parameters:
    - nx, ny: int, Number of nodes along the X and Y axes.
    - spacing: float, Base distance between neighboring nodes.
    - disorder_strength: float, Amplitude of random perturbation (should ideally be < spacing/2).
    
    Returns:
    - verts: (N, 2) array of vertex coordinates.
    - edges: (E, 2) array of edge connections by index.
    """
    verts = []
    
    # 1. Create the base triangular grid
    for j in range(ny):
        for i in range(nx):
            # Shift every other row by half a unit to make triangles
            x = i * spacing + (spacing * 0.5 if j % 2 == 1 else 0)
            y = j * spacing * (np.sqrt(3.0) / 2.0)
            verts.append([x, y])
            
    verts = np.array(verts)
    
    # 2. Add uniform random noise for disorder
    noise = np.random.uniform(-disorder_strength, disorder_strength, size=verts.shape)
    verts += noise
    
    # 3. Use Delaunay triangulation to connect the vertices into a lattice
    tri = Delaunay(verts)
    
    # Extract unique edges from the triangles
    edges_set = set()
    for simplex in tri.simplices:
        for i in range(3):
            u = simplex[i]
            v = simplex[(i + 1) % 3]
            # Keep indices sorted so (0,1) and (1,0) are the same edge
            if u > v:
                u, v = v, u
            edges_set.add((u, v))
            
    edges = np.array(list(edges_set))
    return verts, edges


def generate_2d_spring_constants(num_edges, k=1.0):
    """
    Generates a list of spring constants for the 2D network.
    Defaults to 1.0 for all edges.
    """
    return np.full(num_edges, k)


def pinnedCmat(vertex_positions, edgesByIndex, Cartesian_direction=0, smallest_boolean=True, frac_selected=0.05):
    """
    Constructs a pinned 2D compatibility matrix, and returns the reduced geometry.
    Pins a specified fraction of vertices based on their spatial ranking.
    """
    vertex_positions = np.asarray(vertex_positions)
    edgesByIndex = np.asarray(edgesByIndex)
    
    num_verts = len(vertex_positions)
    num_edges = len(edgesByIndex)
    
    # 1. Edges by endpoints
    p1 = vertex_positions[edgesByIndex[:, 0]]
    p2 = vertex_positions[edgesByIndex[:, 1]]
    
    # 2. Construct normal cMat (2D)
    diff = p1 - p2
    lengths = np.linalg.norm(diff, axis=1, keepdims=True)
    hats = diff / lengths
    
    rows = np.repeat(np.arange(num_edges), 4)
    cols = np.zeros(num_edges * 4, dtype=int)
    data = np.zeros(num_edges * 4)
    
    u = edgesByIndex[:, 0]
    v = edgesByIndex[:, 1]
    
    # 2 DOFs per vertex (x, y)
    cols[0::4] = 2 * u;      cols[1::4] = 2 * u + 1
    cols[2::4] = 2 * v;      cols[3::4] = 2 * v + 1
    
    data[0::4] = hats[:, 0]; data[1::4] = hats[:, 1]
    data[2::4] = -hats[:, 0];data[3::4] = -hats[:, 1]
    
    cMat = csr_matrix((data, (rows, cols)), shape=(num_edges, 2 * num_verts))
    
    # 3. Identify pinned and unpinned vertices based on fraction
    coords = vertex_positions[:, Cartesian_direction]
    num_to_pin = int(round(num_verts * frac_selected))
    sorted_indices = np.argsort(coords)
    
    if smallest_boolean:
        pinned_verts = sorted_indices[:num_to_pin]
    else:
        pinned_verts = sorted_indices[-num_to_pin:]
    
    # Get unpinned vertices
    all_verts = np.arange(num_verts)
    unpinned_vert_indices = np.setdiff1d(all_verts, pinned_verts)
    unpinned_vertex_positions = vertex_positions[unpinned_vert_indices]
    
    # 4. Construct pinned_cMat
    pinned_dofs = []
    for pv in pinned_verts:
        pinned_dofs.extend([2 * pv, 2 * pv + 1])
        
    mask = np.ones(2 * num_verts, dtype=bool)
    mask[pinned_dofs] = False
    remaining_dofs = np.where(mask)[0]
    pinned_cMat = cMat[:, remaining_dofs]
    
    # 5. Filter and Re-index Edges
    old_to_new_map = np.full(num_verts, -1, dtype=int)
    old_to_new_map[unpinned_vert_indices] = np.arange(len(unpinned_vert_indices))
    
    valid_edges_mask = (old_to_new_map[u] != -1) & (old_to_new_map[v] != -1)
    valid_edges_old = edgesByIndex[valid_edges_mask]
    
    unpinned_edges = old_to_new_map[valid_edges_old]
    
    return pinned_cMat, unpinned_vertex_positions, unpinned_edges, valid_edges_mask


def get_imposed_displacements(
    unpinned_vertex_positions, 
    selection_cartesian_direction=0, 
    selection_cartesian_smallest_boolean=False, 
    selection_fraction=0.05, 
    displacement_vector=np.array([0, 10])
):
    """
    Selects a fraction of boundary vertices and assigns a 2D displacement vector to them.
    """
    positions = np.asarray(unpinned_vertex_positions)
    disp_vec = np.asarray(displacement_vector)
    
    num_verts = len(positions)
    num_to_select = int(round(num_verts * selection_fraction))
    
    coords = positions[:, selection_cartesian_direction]
    sorted_indices = np.argsort(coords)
    
    if selection_cartesian_smallest_boolean:
        selected_verts = sorted_indices[:num_to_select]
    else:
        selected_verts = sorted_indices[-num_to_select:]
        
    v_list_dof = []
    for v in selected_verts:
        v_list_dof.extend([2 * v, 2 * v + 1])
        
    v_list_dof = np.array(v_list_dof)
    u_list_flat = np.tile(disp_vec, num_to_select)
    
    return v_list_dof, u_list_flat, selected_verts


def response_to_static_displacements(Cmat, k_list, v_list, u_list):
    """
    Calculates the 2D structural response to static displacements.
    Uses lsqr to find the minimum-norm solution, natively handling 
    singular matrices caused by zero-energy (floppy) modes.
    """
    Cmat = (csr_matrix(Cmat)).T 
    n_total = Cmat.shape[0]
    
    # Diagonals of k_list form the stiffness matrix
    stiffness_mat = diags(np.array(k_list), format='csr')
    d_mat = Cmat @ stiffness_mat @ Cmat.T
    
    v_list = np.array(v_list)
    vb_list = np.setdiff1d(np.arange(n_total), v_list)
    
    daa = d_mat[v_list, :][:, v_list]
    dba = d_mat[vb_list, :][:, v_list]
    dbb = d_mat[vb_list, :][:, vb_list]
    
    ua = np.array(u_list)
    p = -dba @ ua
    u_b = lsqr(dbb, p)[0]
    
    dab = dba.T
    f_a = (daa @ ua) + (dab @ u_b)
    
    # Reshape forces to 2D
    f_a_2d = f_a.reshape(-1, 2)
    total_applied_force = np.sum(f_a_2d, axis=0)
    
    u = np.zeros(n_total)
    u[v_list] = ua
    u[vb_list] = u_b
    
    # Tensions 
    t = stiffness_mat @ Cmat.T @ u
    
    return u, t, total_applied_force


#=================================================================================
#3 - execution
#=================================================================================

# Toggles for features
use_generated_network = True  # Set to False to load from CSV instead

if use_generated_network:
    # Generate a disordered network dynamically
    # nx and ny dictate the grid size, disorder_strength configures the "messiness"
    original_verts, original_edges = generate_disordered_triangular_lattice(
        nx=20, ny=15, spacing=1.0, disorder_strength=0.25
    )
else:
    # Importing data from CSV
    nodes_df = pd.read_csv('nodes_AP.csv')
    edges_df = pd.read_csv('edges_AP.csv')

    # Ensure we are only taking the first 2 columns (X, Y)
    original_verts = nodes_df.to_numpy()[:, :2] 
    original_edges = edges_df.to_numpy()

    # Removing long edges (Specific to CSV network, skip if generating fresh)
    indices_to_remove = [22, 232]
    indices_to_remove = [i for i in indices_to_remove if i < len(original_edges)]
    original_edges = np.delete(original_edges, indices_to_remove, axis=0)


num_edges = len(original_edges)
k_2d_list = generate_2d_spring_constants(num_edges)

# Constructing the compatibility matrix
Cmat, unpinned_verts, unpinned_edges, valid_edges_mask = pinnedCmat(original_verts, original_edges)

active_tensions = np.zeros(1)
all_displacements = np.zeros(1)

# Applying load to network
v_list_dof, u_list_flat, selected_verts = get_imposed_displacements(unpinned_verts)
    
all_displacements, all_tensions, total_applied_force = response_to_static_displacements(
    Cmat, k_2d_list, v_list_dof, u_list_flat)
        
active_tensions = all_tensions[valid_edges_mask]
print("Total applied force:", total_applied_force)



#=================================================================================
#4 - plotting
#=================================================================================

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
ax.set_aspect('equal', adjustable='box') # Keeps geometry undistorted

buffer = 0.1
x_range = original_verts[:, 0].max() - original_verts[:, 0].min()
y_range = original_verts[:, 1].max() - original_verts[:, 1].min()

ax.set_xlim(original_verts[:, 0].min() - buffer * x_range, original_verts[:, 0].max() + buffer * x_range)
ax.set_ylim(original_verts[:, 1].min() - buffer * y_range, original_verts[:, 1].max() + buffer * y_range)

plt.tight_layout()
plt.show()
