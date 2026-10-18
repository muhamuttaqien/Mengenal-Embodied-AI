# Import time untuk mengatur kecepatan simulasi.
import time

# Import MuJoCo.
import mujoco

# Import viewer bawaan MuJoCo.
import mujoco.viewer


# Menyimpan model MJCF sederhana dalam bentuk string.
MODEL_XML = """
<mujoco model="mujoco_basics">
    <option timestep="0.01"/>
    <worldbody>
        <geom name="floor"
              type="plane"
              size="2 2 0.1"/>
        <body name="pendulum"
              pos="0 0 1">
            <joint name="hinge"
                   type="hinge"
                   axis="0 1 0"/>
            <geom name="link"
                  type="capsule"
                  fromto="0 0 0 0 0 -0.6"
                  size="0.06"
                  mass="1"/>
        </body>
    </worldbody>
    <actuator>
        <motor name="motor"
               joint="hinge"
               gear="1"/>
    </actuator>
</mujoco>
"""


# Membuat model MuJoCo dari MJCF.
model = mujoco.MjModel.from_xml_string(
    MODEL_XML
)


# Membuat data simulasi untuk model.
data = mujoco.MjData(
    model
)


# Menampilkan posisi joint awal.
print(
    "Initial qpos:",
    data.qpos.copy()
)


# Menampilkan kecepatan joint awal.
print(
    "Initial qvel:",
    data.qvel.copy()
)


# Membuka viewer MuJoCo.
with mujoco.viewer.launch_passive(
    model,
    data
) as viewer:

    # Menjalankan simulasi selama lima detik.
    while (
        viewer.is_running()
        and data.time < 5.0
    ):

        # Memberikan command motor positif
        # selama 2,5 detik pertama.
        if data.time < 2.5:

            data.ctrl[0] = 0.5

        # Memberikan command motor negatif
        # selama 2,5 detik berikutnya.
        else:

            data.ctrl[0] = -0.5


        # Menjalankan satu physics step.
        mujoco.mj_step(
            model,
            data
        )


        # Memperbarui tampilan viewer.
        viewer.sync()


        # Menyesuaikan kecepatan simulasi.
        time.sleep(
            model.opt.timestep
        )


# Menampilkan posisi joint akhir.
print(
    "Final qpos  :",
    data.qpos.copy()
)


# Menampilkan kecepatan joint akhir.
print(
    "Final qvel  :",
    data.qvel.copy()
)
