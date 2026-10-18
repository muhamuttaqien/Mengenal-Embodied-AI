# Menentukan label action robot.
LEFT = 0
FORWARD = 1
RIGHT = 2

# Menentukan nama setiap action.
ACTION_NAMES = [
    "LEFT",
    "FORWARD",
    "RIGHT",
]

# Menentukan jarak aman di depan robot.
SAFE_DISTANCE = 0.60


def rule_based_action(
    left_distance,
    front_distance,
    right_distance,
):
    # Bergerak maju jika bagian depan cukup aman.
    if front_distance >= SAFE_DISTANCE:
        return FORWARD

    # Belok ke kiri jika ruang kiri lebih besar.
    if left_distance > right_distance:
        return LEFT

    # Belok ke kanan pada kondisi lainnya.
    return RIGHT
