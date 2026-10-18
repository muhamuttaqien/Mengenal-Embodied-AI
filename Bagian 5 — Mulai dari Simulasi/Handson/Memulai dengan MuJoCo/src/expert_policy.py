# Import NumPy.
import numpy as np

# Import helper untuk membaca
# state simulator.
from src.observation_utils import (
    get_can_position,
    get_eef_position,
    get_target_position,
)


# Gripper command.
OPEN_GRIPPER = -1.0
CLOSE_GRIPPER = 1.0


class PickPlaceScriptedExpert:

    def __init__(self):

        # Phase awal.
        self.phase = "APPROACH"

        # Counter timestep
        # pada phase saat ini.
        self.phase_steps = 0

        # Target lift disimpan sekali.
        self.lift_target = None

        # Target retreat disimpan sekali.
        self.retreat_target = None

        # Tinggi object ketika
        # grasp selesai.
        self.grasp_can_z = None


    def reset(self):

        self.phase = "APPROACH"

        self.phase_steps = 0

        self.lift_target = None

        self.retreat_target = None

        self.grasp_can_z = None


    # Mengganti phase.
    def _set_phase(
        self,
        phase,
    ):

        self.phase = phase

        self.phase_steps = 0

        print(
            "→ New phase:",
            phase
        )


    # Membuat action Cartesian.
    def _move_action(
        self,
        eef_position,
        target_position,
        gripper,
        gain=8.0,
    ):

        # Action Panda OSC_POSE:
        #
        # [
        #   dx,
        #   dy,
        #   dz,
        #   droll,
        #   dpitch,
        #   dyaw,
        #   gripper
        # ]

        action = np.zeros(
            7,
            dtype=np.float32,
        )


        # Error posisi.
        delta_position = (
            target_position
            - eef_position
        )


        # Mengubah error menjadi
        # normalized control command.
        action[:3] = np.clip(
            delta_position * gain,
            -1.0,
            1.0,
        )


        # Orientation tidak diubah.
        action[3:6] = 0.0


        # Gripper command.
        action[6] = gripper


        return action


    # Menghasilkan satu expert action.
    def act(
        self,
        observation,
        env,
    ):

        # Posisi EEF.
        eef_position = (
            get_eef_position(
                observation
            )
        )


        # Posisi Can.
        can_position = (
            get_can_position(
                observation
            )
        )


        # Target bin.
        target_position = (
            get_target_position(
                env
            )
        )


        # ==========================
        # Object approach target
        # ==========================

        approach_position = (
            can_position
            + np.array(
                [
                    0.0,
                    0.0,
                    0.12,
                ],
                dtype=np.float32,
            )
        )


        # ==========================
        # Grasp target
        # ==========================

        grasp_position = (
            can_position
            + np.array(
                [
                    0.0,
                    0.0,
                    0.015,
                ],
                dtype=np.float32,
            )
        )


        # ==========================
        # Target above destination
        # ==========================

        target_above = (
            target_position
            + np.array(
                [
                    0.0,
                    0.0,
                    0.18,
                ],
                dtype=np.float32,
            )
        )


        # ==========================
        # Placement target
        # ==========================

        target_place = (
            target_position
            + np.array(
                [
                    0.0,
                    0.0,
                    0.06,
                ],
                dtype=np.float32,
            )
        )


        # Tambah timestep phase.
        self.phase_steps += 1


        # ==========================
        # APPROACH
        # ==========================

        if self.phase == "APPROACH":

            action = self._move_action(
                eef_position,
                approach_position,
                OPEN_GRIPPER,
            )


            error = np.linalg.norm(
                eef_position
                - approach_position
            )


            if error < 0.025:

                self._set_phase(
                    "DESCEND"
                )


            return action


        # ==========================
        # DESCEND
        # ==========================

        if self.phase == "DESCEND":

            action = self._move_action(
                eef_position,
                grasp_position,
                OPEN_GRIPPER,
            )


            error = np.linalg.norm(
                eef_position
                - grasp_position
            )


            if error < 0.018:

                self._set_phase(
                    "GRASP"
                )


            return action


        # ==========================
        # GRASP
        # ==========================

        if self.phase == "GRASP":

            # Arm tidak bergerak.
            action = np.zeros(
                7,
                dtype=np.float32,
            )


            # Tutup gripper.
            action[6] = CLOSE_GRIPPER


            # Tunggu agar grasp stabil.
            if self.phase_steps >= 15:

                # Simpan tinggi Can
                # ketika grasp selesai.
                self.grasp_can_z = float(
                    can_position[2]
                )


                # Buat target lift SEKALI.
                self.lift_target = (
                    eef_position.copy()
                    + np.array(
                        [
                            0.0,
                            0.0,
                            0.15,
                        ],
                        dtype=np.float32,
                    )
                )


                self._set_phase(
                    "LIFT"
                )


            return action


        # ==========================
        # LIFT
        # ==========================

        if self.phase == "LIFT":

            action = self._move_action(
                eef_position,
                self.lift_target,
                CLOSE_GRIPPER,
            )


            # Mengukur kenaikan
            # posisi object.
            object_lift = (
                float(
                    can_position[2]
                )
                - self.grasp_can_z
            )


            # Error EEF terhadap
            # target lift.
            eef_error = (
                np.linalg.norm(
                    eef_position
                    - self.lift_target
                )
            )


            # Lift dianggap berhasil
            # jika object naik 10 cm
            # ATAU EEF sudah dekat target.
            if (
                object_lift >= 0.10
                or eef_error < 0.05
            ):

                self._set_phase(
                    "MOVE_TO_TARGET"
                )


            return action


        # ==========================
        # MOVE TO TARGET
        # ==========================

        if self.phase == "MOVE_TO_TARGET":

            action = self._move_action(
                eef_position,
                target_above,
                CLOSE_GRIPPER,
            )


            error = np.linalg.norm(
                eef_position
                - target_above
            )


            if error < 0.05:

                self._set_phase(
                    "PLACE"
                )


            return action


        # ==========================
        # PLACE
        # ==========================

        if self.phase == "PLACE":

            action = self._move_action(
                eef_position,
                target_place,
                CLOSE_GRIPPER,
            )


            error = np.linalg.norm(
                eef_position
                - target_place
            )


            if error < 0.04:

                self._set_phase(
                    "RELEASE"
                )


            return action


        # ==========================
        # RELEASE
        # ==========================

        if self.phase == "RELEASE":

            action = np.zeros(
                7,
                dtype=np.float32,
            )


            # Buka gripper.
            action[6] = OPEN_GRIPPER


            # Tunggu object terlepas.
            if self.phase_steps >= 15:

                # Buat target retreat sekali.
                self.retreat_target = (
                    eef_position.copy()
                    + np.array(
                        [
                            0.0,
                            0.0,
                            0.10,
                        ],
                        dtype=np.float32,
                    )
                )


                self._set_phase(
                    "RETREAT"
                )


            return action


        # ==========================
        # RETREAT
        # ==========================

        if self.phase == "RETREAT":

            action = self._move_action(
                eef_position,
                self.retreat_target,
                OPEN_GRIPPER,
                gain=5.0,
            )


            error = np.linalg.norm(
                eef_position
                - self.retreat_target
            )


            if (
                error < 0.04
                or self.phase_steps >= 40
            ):

                self._set_phase(
                    "DONE"
                )


            return action


        # ==========================
        # DONE
        # ==========================

        action = np.zeros(
            7,
            dtype=np.float32,
        )


        action[6] = OPEN_GRIPPER


        return action
