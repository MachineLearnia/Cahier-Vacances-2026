import matplotlib.pyplot as plt
import pandas as pd

# la France en latitude/longitude n'est pas "carrée" : ce ratio corrige la carte
MAP_ASPECT_RATIO = 1.4

# 21 couleurs bien distinctes pour les 21 étapes (tab20 de matplotlib + une bonus)
STAGE_COLORS = list(plt.get_cmap("tab20").colors) + ["#4d4d4d"]

# Contour de la France métropolitaine (longitude, latitude), issu d'un fond de
# carte IGN simplifié. Deux polygones : le continent et la Corse. On les stocke
# ici (et non dans un fichier externe) pour que `utils.py` reste autonome.
FRANCE_MAINLAND = [
    (7.1303, 47.503), (6.9825, 47.4935), (7.0019, 47.4539), (6.8793, 47.3524),
    (7.0156, 47.3728), (7.0568, 47.3346), (6.9409, 47.2867), (6.9554, 47.2433),
    (6.7028, 47.0816), (6.7186, 47.0508), (6.4327, 46.9286), (6.4522, 46.7741),
    (6.1116, 46.5776), (6.1565, 46.5455), (6.064, 46.4162), (6.1702, 46.3665),
    (6.1024, 46.2848), (6.1242, 46.251), (5.9747, 46.2151), (5.9561, 46.1321),
    (6.1362, 46.1415), (6.2945, 46.2249), (6.3095, 46.2563), (6.2376, 46.2777),
    (6.3052, 46.3668), (6.3891, 46.3401), (6.5131, 46.4048), (6.8053, 46.3941),
    (6.772, 46.3503), (6.8645, 46.2796), (6.7965, 46.1386), (6.8999, 46.1239),
    (6.8756, 46.0477), (6.9379, 46.0633), (7.0451, 45.9224), (6.9414, 45.8469),
    (6.8189, 45.8362), (6.8084, 45.7251), (7.0007, 45.6399), (7.0003, 45.5044),
    (7.1859, 45.4032), (7.0799, 45.2128), (6.6267, 45.1038), (6.6739, 45.0196),
    (6.7454, 45.0143), (6.7507, 44.9057), (7.0238, 44.8231), (6.9994, 44.7897),
    (7.0771, 44.6809), (6.9632, 44.6781), (6.9684, 44.6198), (6.8534, 44.5288),
    (6.9481, 44.4297), (6.8929, 44.4208), (6.8874, 44.361), (7.0085, 44.2352),
    (7.358, 44.116), (7.6846, 44.174), (7.7144, 44.0612), (7.4979, 43.8717),
    (7.5292, 43.784), (7.3313, 43.6745), (7.3147, 43.7065), (7.157, 43.6535),
    (7.1364, 43.5446), (6.9633, 43.5422), (6.8563, 43.4115), (6.7455, 43.4179),
    (6.7165, 43.3475), (6.5839, 43.2773), (6.6976, 43.2665), (6.6466, 43.1677),
    (6.3845, 43.144), (6.3643, 43.0863), (6.201, 43.1161), (6.1488, 43.0259),
    (6.0913, 43.0354), (6.1316, 43.048), (6.114, 43.0837), (5.9206, 43.1239),
    (5.8805, 43.105), (5.947, 43.0677), (5.8288, 43.0494), (5.8082, 43.1152),
    (5.6867, 43.1797), (5.3418, 43.2126), (5.3735, 43.2942), (5.3142, 43.36),
    (5.0502, 43.325), (4.97, 43.4249), (4.8935, 43.4041), (4.8608, 43.454),
    (4.8773, 43.4105), (4.8244, 43.4244), (4.8718, 43.39), (4.8289, 43.3759),
    (4.9175, 43.3799), (4.8551, 43.3326), (4.6591, 43.3462), (4.5607, 43.374),
    (4.593, 43.4099), (4.5549, 43.4462), (4.1837, 43.4676), (4.1231, 43.4942),
    (4.1216, 43.5471), (4.007, 43.5517), (3.6431, 43.3831), (3.5095, 43.2717),
    (3.4085, 43.2887), (3.2871, 43.242), (3.1072, 43.0892), (3.0425, 42.959),
    (3.0245, 42.7039), (3.0518, 42.544), (3.1411, 42.5152), (3.1736, 42.4359),
    (2.9471, 42.4818), (2.6739, 42.4047), (2.6755, 42.3424), (2.5327, 42.3331),
    (2.2567, 42.4384), (2.0154, 42.3468), (1.9369, 42.4536), (1.7307, 42.4928),
    (1.7866, 42.5743), (1.7361, 42.6172), (1.4937, 42.6532), (1.4378, 42.6032),
    (1.3574, 42.7194), (1.1659, 42.7087), (1.0791, 42.7883), (0.7084, 42.8614),
    (0.6454, 42.7835), (0.6684, 42.6895), (0.3601, 42.7243), (0.2951, 42.6732),
    (0.1757, 42.737), (-0.0166, 42.6849), (-0.3134, 42.8494), (-0.5669, 42.7805),
    (-0.7319, 42.8961), (-0.753, 42.9677), (-0.9438, 42.9532), (-1.1422, 43.008),
    (-1.3093, 43.0686), (-1.2702, 43.1186), (-1.3451, 43.094), (-1.3537, 43.0282),
    (-1.4412, 43.0463), (-1.4732, 43.0868), (-1.3817, 43.1896), (-1.3885, 43.2586),
    (-1.5353, 43.2946), (-1.6087, 43.2519), (-1.6241, 43.3061), (-1.7297, 43.2957),
    (-1.7888, 43.3784), (-1.6045, 43.4304), (-1.4468, 43.6456), (-1.3065, 44.1706),
    (-1.2586, 44.5471), (-1.1915, 44.6607), (-1.0036, 44.6484), (-1.1676, 44.776),
    (-1.262, 44.6322), (-1.1562, 45.4761), (-1.0912, 45.5624), (-0.9892, 45.5813),
    (-1.2372, 45.7059), (-1.2426, 45.7816), (-1.1337, 45.8028), (-1.1702, 45.8559),
    (-1.1136, 45.8593), (-1.0643, 45.9499), (-1.1215, 46.003), (-1.0631, 45.9944),
    (-1.0561, 46.0342), (-1.1282, 46.1266), (-1.242, 46.1574), (-1.1148, 46.2916),
    (-1.2031, 46.3157), (-1.2074, 46.2666), (-1.2959, 46.3239), (-1.2937, 46.2887),
    (-1.3431, 46.3428), (-1.4659, 46.3424), (-1.5151, 46.4043), (-1.8123, 46.4934),
    (-1.857, 46.6099), (-2.1421, 46.8191), (-2.155, 46.8897), (-1.9804, 47.0289),
    (-2.1034, 47.1144), (-2.2472, 47.1325), (-2.1671, 47.1662), (-2.17, 47.2685),
    (-2.2982, 47.2331), (-2.5464, 47.2906), (-2.5029, 47.3287), (-2.5581, 47.3757),
    (-2.4316, 47.4158), (-2.501, 47.4927), (-2.4205, 47.4953), (-2.6319, 47.5046),
    (-2.5591, 47.5518), (-2.6044, 47.531), (-2.6106, 47.5676), (-2.6749, 47.4919),
    (-2.8153, 47.4866), (-2.9145, 47.5574), (-2.7346, 47.5409), (-2.6898, 47.6373),
    (-2.7212, 47.59), (-2.7941, 47.645), (-2.8905, 47.5742), (-2.9783, 47.6591),
    (-2.9266, 47.5569), (-3.127, 47.5984), (-3.081, 47.4704), (-3.133, 47.475),
    (-3.1397, 47.5796), (-3.2109, 47.643), (-3.1031, 47.7182), (-3.1526, 47.7189),
    (-3.1348, 47.7473), (-3.2008, 47.7449), (-3.1657, 47.7045), (-3.2163, 47.6958),
    (-3.2146, 47.6449), (-3.3593, 47.6869), (-3.2776, 47.6903), (-3.3654, 47.7103),
    (-3.2777, 47.7944), (-3.3443, 47.7416), (-3.3885, 47.8283), (-3.3558, 47.7324),
    (-3.4501, 47.6951), (-3.5286, 47.7654), (-3.5421, 47.8628), (-3.5386, 47.7626),
    (-3.6808, 47.7768), (-3.7226, 47.8034), (-3.6412, 47.8284), (-3.7327, 47.8035),
    (-3.7518, 47.8472), (-3.742, 47.7975), (-3.8561, 47.7896), (-3.8806, 47.8592),
    (-3.9773, 47.9097), (-3.9771, 47.8538), (-4.0994, 47.8625), (-4.1447, 47.9093),
    (-4.0777, 47.9374), (-4.1172, 47.9835), (-4.1108, 47.9364), (-4.1763, 47.9071),
    (-4.1133, 47.862), (-4.2157, 47.866), (-4.1588, 47.8315), (-4.183, 47.8002),
    (-4.3742, 47.798), (-4.346, 47.8402), (-4.3836, 47.9209), (-4.5367, 48.0116),
    (-4.4882, 48.0384), (-4.5648, 47.9998), (-4.7408, 48.0406), (-4.3044, 48.0894),
    (-4.2731, 48.1542), (-4.4639, 48.2394), (-4.5541, 48.1678), (-4.5433, 48.2491),
    (-4.6294, 48.2808), (-4.5699, 48.2819), (-4.5826, 48.3194), (-4.5344, 48.3419),
    (-4.5358, 48.2839), (-4.2724, 48.296), (-4.2662, 48.2573), (-4.1169, 48.2183),
    (-4.0969, 48.2555), (-4.2794, 48.2778), (-4.1874, 48.2952), (-4.3332, 48.3131),
    (-4.2645, 48.3582), (-4.4574, 48.3271), (-4.2701, 48.445), (-4.7167, 48.3296),
    (-4.7737, 48.3303), (-4.7461, 48.3657), (-4.7864, 48.3613), (-4.7954, 48.4147),
    (-4.7196, 48.4756), (-4.776, 48.5192), (-4.7044, 48.57), (-4.5053, 48.5459),
    (-4.6123, 48.5782), (-4.5983, 48.608), (-4.4784, 48.573), (-4.5683, 48.6091),
    (-4.5438, 48.6365), (-4.3298, 48.6771), (-4.2969, 48.6326), (-4.1293, 48.6969),
    (-4.0558, 48.6711), (-3.9709, 48.7273), (-3.9563, 48.6159), (-3.9221, 48.6755),
    (-3.8515, 48.6067), (-3.8209, 48.7182), (-3.6433, 48.6959), (-3.6591, 48.6592),
    (-3.573, 48.6749), (-3.5496, 48.7467), (-3.5859, 48.7774), (-3.5035, 48.8387),
    (-3.3975, 48.8008), (-3.2245, 48.8699), (-3.2197, 48.7838), (-3.0742, 48.882),
    (-3.1235, 48.7601), (-3.0728, 48.8204), (-3.009, 48.8197), (-3.0464, 48.7856),
    (-2.9285, 48.7548), (-2.9451, 48.7208), (-2.6816, 48.4917), (-2.6821, 48.532),
    (-2.6303, 48.5261), (-2.4879, 48.6452), (-2.3177, 48.6887), (-2.2852, 48.6645),
    (-2.3359, 48.62), (-2.2474, 48.6461), (-2.2129, 48.5728), (-2.1237, 48.6044),
    (-2.1507, 48.6347), (-2.0473, 48.6379), (-1.9737, 48.5441), (-2.0017, 48.4917),
    (-1.9482, 48.5192), (-1.987, 48.5845), (-1.9542, 48.579), (-2.0286, 48.6503),
    (-1.9371, 48.7023), (-1.8451, 48.7118), (-1.8687, 48.6381), (-1.7677, 48.6024),
    (-1.3518, 48.6312), (-1.3996, 48.6555), (-1.3761, 48.6904), (-1.4458, 48.6548),
    (-1.571, 48.7442), (-1.5744, 48.8217), (-1.6144, 48.8342), (-1.5567, 48.9323),
    (-1.5499, 48.8964), (-1.5568, 49.0266), (-1.5055, 49.0204), (-1.5601, 49.0367),
    (-1.5762, 49.0004), (-1.5989, 49.0374), (-1.6136, 49.2188), (-1.5686, 49.2216),
    (-1.6255, 49.2101), (-1.7112, 49.3251), (-1.6746, 49.332), (-1.8092, 49.3721),
    (-1.8866, 49.5264), (-1.8458, 49.6215), (-1.9469, 49.6745), (-1.9422, 49.7261),
    (-1.6152, 49.6435), (-1.4733, 49.697), (-1.2662, 49.6954), (-1.2287, 49.6061),
    (-1.3075, 49.5418), (-1.1361, 49.354), (-0.9472, 49.3958), (-0.2257, 49.2818),
    (-0.0872, 49.2979), (0.1298, 49.403), (0.3406, 49.4343), (0.1212, 49.4632),
    (0.0665, 49.5101), (0.206, 49.7142), (0.5835, 49.8526), (1.1945, 49.968),
    (1.4434, 50.1005), (1.5484, 50.2152), (1.6816, 50.1808), (1.5384, 50.2786),
    (1.5558, 50.3613), (1.6415, 50.3522), (1.5557, 50.3977), (1.583, 50.5346),
    (1.6592, 50.5078), (1.5766, 50.5722), (1.5818, 50.871), (1.7807, 50.9549),
    (2.1221, 50.9905), (2.1504, 51.0343), (2.1797, 51.0074), (2.1714, 51.0443),
    (2.5455, 51.089), (2.6327, 50.946), (2.59, 50.9191), (2.5991, 50.8488),
    (2.7239, 50.8101), (2.7896, 50.7263), (2.9061, 50.6923), (2.9505, 50.7513),
    (3.1508, 50.7901), (3.2612, 50.7013), (3.2887, 50.5255), (3.6084, 50.4967),
    (3.7104, 50.3032), (3.7474, 50.3509), (4.0237, 50.3589), (4.1354, 50.2572),
    (4.208, 50.273), (4.1269, 50.135), (4.197, 50.1353), (4.2308, 50.0733),
    (4.1358, 50.0194), (4.1963, 49.9553), (4.4469, 49.9375), (4.6936, 49.9955),
    (4.693, 50.0848), (4.8251, 50.1691), (4.8971, 50.1378), (4.7901, 49.97),
    (4.89, 49.9093), (4.8515, 49.7936), (4.9954, 49.8006), (5.1662, 49.6929),
    (5.2707, 49.6953), (5.332, 49.6548), (5.3121, 49.6117), (5.4286, 49.5959),
    (5.4652, 49.4989), (5.7714, 49.5632), (6.0422, 49.4478), (6.2407, 49.5145),
    (6.5419, 49.4324), (6.6018, 49.3665), (6.5658, 49.3473), (6.6704, 49.2803),
    (6.7385, 49.1637), (6.8345, 49.1515), (6.8378, 49.2133), (6.9254, 49.2236),
    (7.035, 49.1906), (7.0543, 49.1126), (7.1009, 49.1556), (7.2937, 49.1151),
    (7.4448, 49.1842), (7.6353, 49.0542), (7.9338, 49.058), (8.2249, 48.9754),
    (8.0915, 48.8057), (7.8398, 48.6414), (7.7336, 48.3987), (7.7447, 48.3278),
    (7.5773, 48.1204), (7.5687, 48.0341), (7.6221, 47.9723), (7.5118, 47.697),
    (7.5849, 47.5756), (7.3856, 47.4316), (7.2462, 47.4202), (7.1708, 47.443),
    (7.2011, 47.4939), (7.1303, 47.503),
]

CORSICA = [
    (9.4023, 41.8587), (9.3855, 41.6463), (9.2809, 41.5972), (9.368, 41.5912),
    (9.2725, 41.5288), (9.2878, 41.4838), (9.2154, 41.4144), (9.2597, 41.4137),
    (9.22, 41.3674), (9.0965, 41.3921), (9.1224, 41.4415), (9.0701, 41.4446),
    (9.0799, 41.4775), (9.0418, 41.4568), (8.92, 41.4891), (8.7822, 41.5663),
    (8.7943, 41.6327), (8.8724, 41.6472), (8.9135, 41.691), (8.7828, 41.6992),
    (8.775, 41.7414), (8.6587, 41.7403), (8.728, 41.7739), (8.7108, 41.801),
    (8.7713, 41.8112), (8.7845, 41.8311), (8.7509, 41.8452), (8.7882, 41.8505),
    (8.8026, 41.8965), (8.7524, 41.9334), (8.6066, 41.8952), (8.6234, 41.9348),
    (8.5921, 41.9644), (8.6629, 41.9765), (8.66, 42.0123), (8.7465, 42.0511),
    (8.7003, 42.1123), (8.6589, 42.1013), (8.5588, 42.1463), (8.5934, 42.1683),
    (8.5611, 42.1716), (8.5814, 42.2059), (8.5397, 42.2371), (8.6928, 42.2683),
    (8.6016, 42.309), (8.6149, 42.3496), (8.5578, 42.3322), (8.5432, 42.3673),
    (8.6568, 42.4168), (8.6655, 42.5136), (8.7202, 42.5254), (8.7092, 42.5767),
    (8.7811, 42.5565), (8.8026, 42.6026), (9.015, 42.6414), (9.1246, 42.7316),
    (9.2211, 42.7357), (9.2875, 42.6745), (9.3142, 42.689), (9.3456, 42.7433),
    (9.3095, 42.8338), (9.3403, 42.8657), (9.3214, 42.8969), (9.3615, 42.9248),
    (9.3402, 42.9931), (9.4199, 43.0116), (9.4635, 42.9864), (9.4928, 42.8059),
    (9.4462, 42.6736), (9.5327, 42.548), (9.5591, 42.1967), (9.55, 42.1042),
    (9.417, 41.9612), (9.4023, 41.8587),
]

FRANCE_OUTLINE = [FRANCE_MAINLAND, CORSICA]


def _draw_france(ax):
    """Draw the outline of metropolitan France as a soft background on ax.

    Arguments:
    ax -- matplotlib Axes on which to draw the outline
    """
    for polygon in FRANCE_OUTLINE:
        lons = [point[0] for point in polygon]
        lats = [point[1] for point in polygon]
        ax.fill(lons, lats, color="#eef3ee", zorder=0)
        ax.plot(lons, lats, color="darkgreen", linewidth=1, alpha=0.4, zorder=1)


def load_villages(path="villages_2027.csv"):
    """Load the 120 stage villages selected for the 2027 Tour de France.

    Arguments:
    path -- location of the villages CSV file

    Returns:
    villages -- DataFrame with columns village, departement, latitude, longitude
    """
    try:
        villages = pd.read_csv(path, dtype={"departement": str})
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Le fichier '{path}' est introuvable. Il est fourni avec le projet : "
            "vérifie que tu exécutes bien le notebook depuis le dossier Projet_03."
        ) from None
    return villages


def plot_villages(villages, title="Les 120 villages-étapes du Tour 2027"):
    """Draw the villages on a latitude/longitude scatter plot.

    Arguments:
    villages -- DataFrame with latitude and longitude columns
    title -- title of the figure
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    _draw_france(ax)
    ax.scatter(villages["longitude"], villages["latitude"], s=25, color="darkgreen", zorder=3)
    ax.set_aspect(MAP_ASPECT_RATIO)
    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(alpha=0.2)
    plt.tight_layout()
    plt.show()


def plot_stages(villages, labels, title, numbered=False):
    """Draw the villages colored by their stage assignment.

    Arguments:
    villages -- DataFrame with latitude and longitude columns
    labels -- array-like of cluster/stage labels, one per village
    title -- title of the figure
    numbered -- if True, write the stage number at the center of each stage
    """
    labels = pd.Series(list(labels), index=villages.index)

    fig, ax = plt.subplots(figsize=(8, 8))
    _draw_france(ax)
    for rank, stage in enumerate(sorted(labels.unique())):
        mask = labels == stage
        color = STAGE_COLORS[rank % len(STAGE_COLORS)]
        ax.scatter(villages.loc[mask, "longitude"], villages.loc[mask, "latitude"],
                   s=30, color=color, zorder=3)
        if numbered:
            ax.annotate(str(stage),
                        (villages.loc[mask, "longitude"].mean(), villages.loc[mask, "latitude"].mean()),
                        fontsize=9, fontweight="bold", ha="center", va="center", zorder=5,
                        bbox=dict(boxstyle="circle,pad=0.25", facecolor="white",
                                  edgecolor=color, linewidth=1.5))
    ax.set_aspect(MAP_ASPECT_RATIO)
    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(alpha=0.2)
    plt.tight_layout()
    plt.show()


def plot_final_tour(villages, stage_paths, stage_distances):
    """Draw the complete Tour: every stage path in its own color, numbered.

    Arguments:
    villages -- DataFrame with latitude and longitude columns
    stage_paths -- dict {stage_number: list of village indices in visiting order}
    stage_distances -- dict {stage_number: stage length in kilometers}
    """
    fig, ax = plt.subplots(figsize=(9, 9))
    _draw_france(ax)
    for stage in sorted(stage_paths):
        path = stage_paths[stage]
        color = STAGE_COLORS[(stage - 1) % len(STAGE_COLORS)]
        lons = [villages["longitude"].iloc[i] for i in path]
        lats = [villages["latitude"].iloc[i] for i in path]
        ax.plot(lons, lats, color=color, linewidth=2, zorder=2)
        ax.scatter(lons, lats, s=20, color=color, zorder=3)
        ax.annotate(str(stage), (sum(lons) / len(lons), sum(lats) / len(lats)),
                    fontsize=9, fontweight="bold", ha="center", va="center", zorder=5,
                    bbox=dict(boxstyle="circle,pad=0.25", facecolor="white",
                              edgecolor=color, linewidth=1.5))
    total = sum(stage_distances.values())
    ax.set_aspect(MAP_ASPECT_RATIO)
    ax.set_title(f"Tour de France 2027 : 21 étapes, {total:.0f} km au total")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(alpha=0.2)
    plt.tight_layout()
    plt.show()


def plot_stage_zoom(villages, path, stage_number, distance):
    """Draw a single stage zoomed in, with village names and start/finish markers.

    Arguments:
    villages -- DataFrame with village, latitude and longitude columns
    path -- list of village indices, in visiting order
    stage_number -- number of the stage (for the title)
    distance -- length of the stage in kilometers (for the title)
    """
    lons = [villages["longitude"].iloc[i] for i in path]
    lats = [villages["latitude"].iloc[i] for i in path]
    names = [villages["village"].iloc[i] for i in path]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(lons, lats, color="steelblue", linewidth=2, zorder=2)
    ax.scatter(lons, lats, s=45, color="steelblue", zorder=3)
    ax.scatter([lons[0]], [lats[0]], s=160, color="gold", edgecolor="black",
               zorder=4, label="Départ")
    ax.scatter([lons[-1]], [lats[-1]], s=160, color="black", marker="s",
               zorder=4, label="Arrivée")
    for lon, lat, name in zip(lons, lats, names):
        ax.annotate(name, (lon, lat), textcoords="offset points", xytext=(6, 6),
                    fontsize=8, zorder=5)
    ax.set_aspect(MAP_ASPECT_RATIO)
    ax.set_title(f"Étape {stage_number} : {names[0]} -> {names[-1]}, {distance:.0f} km")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(alpha=0.2)
    ax.legend()
    plt.tight_layout()
    plt.show()


def print_roadbook(villages, stage_paths, stage_distances):
    """Pretty-print the official roadbook of the Tour, stage by stage.

    Arguments:
    villages -- DataFrame with a village column
    stage_paths -- dict {stage_number: list of village indices in visiting order}
    stage_distances -- dict {stage_number: stage length in kilometers}
    """
    total = sum(stage_distances.values())
    longest = max(stage_distances, key=stage_distances.get)
    shortest = min(stage_distances, key=stage_distances.get)

    print("=" * 78)
    print("🚴  LIVRE DE ROUTE OFFICIEL - TOUR DE FRANCE 2027  🚴".center(78))
    print("=" * 78)
    for stage in sorted(stage_paths):
        path = stage_paths[stage]
        start = villages["village"].iloc[path[0]]
        finish = villages["village"].iloc[path[-1]]
        badge = ""
        if stage == longest:
            badge = "  🏔 étape reine"
        elif stage == shortest:
            badge = "  ⏱ la plus courte"
        line = f"Étape {stage:>2} | {start} -> {finish}"
        print(f"{line:<58} | {len(path):>2} villages | {stage_distances[stage]:>4.0f} km{badge}")
    print("-" * 78)
    print(f"{'TOTAL':<58} | {sum(len(p) for p in stage_paths.values()):>2} villages | {total:>4.0f} km")
    print("=" * 78)
