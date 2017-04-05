docker run -it \
  --net host \
  --cpuset-cpus 0 \
  --memory 1gb \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /home/v:/home/v \
  -e DISPLAY=unix$DISPLAY \
  -e XAUTHORITY=$XAUTHORITY \
  -v $HOME/Downloads:/root/Downloads \
  -v $HOME/.config/google-chrome/:/data \
  -v /dev/shm \
  -v /sys/fs/cgroup:/sys/fs/cgroup \
  --device /dev/snd \
  --name chrome \
  --privileged \
  --cap-add CAP_SYS_ADMIN \
  /usr/bin/google-chrome
