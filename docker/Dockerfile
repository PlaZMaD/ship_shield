FROM olantwin/ship-base:201120
COPY . /ship
RUN git clone https://github.com/ShipSoft/FairShip.git
RUN chmod +x /ship/run_simulation.sh && chmod +x /ship/get_params.sh && yum -y install vim
COPY azcopy /bin/azcopy
WORKDIR /ship
RUN mkdir ./shield_files ./muon_input && chmod +x /bin/azcopy
COPY muons_optimisation_input.root ./muon_input/reweighted_input_test.root
RUN mkdir ./shield_files/geometry/ && mkdir ./shield_files/outputs/
COPY fs_mods/fluxDet /FairShip/fluxDet
RUN python3 ./fs_mods/fs_mod.py
WORKDIR /
RUN aliBuild -c shipdist/ --defaults fairship build FairShip --no-local ROOT
WORKDIR /ship
ENTRYPOINT ./run_simulation.sh | tee /ship/shield_files/outputs/logs
