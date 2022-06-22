import hlt
import logging
from collections import OrderedDict
game = hlt.Game("Basic Bot3 ")
logging.info("Starting my Faster bot!")

while True:
    Map = game.update_map()
    commands = []
    Planet_has_been_attacked = []
 
    alltroops = Map.get_me().all_ships()

    for arrmy in alltroops:

        targetplanet = []
        targetarrmy = []
        if arrmy.docking_status != arrmy.DockingStatus.UNDOCKED:
            continue

        entities_by_distance_all = Map.nearby_entities_by_distance(arrmy)
        entities_by_distance_all = sorted(
            entities_by_distance_all.items(), key=lambda entities_by_distance_allX: entities_by_distance_allX[0], reverse=False)

        for target in entities_by_distance_all:

            if isinstance(target[1][0], hlt.entity.Planet) and not target[1][0].is_owned():
                targetplanet.append(target[1][0])
            else:
                if not (target[1][0] in alltroops):
                    targetarrmy.append(target)

        logging.info(targetplanet)
        logging.info(targetarrmy)

        for planet in targetplanet:
            if arrmy.can_dock(planet):
                commands.append(arrmy.dock(planet))
                break
            else:
                if planet in Planet_has_been_attacked:
                    continue
                else:

                    navigate_command = arrmy.navigate(
                        arrmy.closest_point_to(planet),
                        Map,
                        speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=False)

                    if navigate_command:
                        commands.append(navigate_command)
                        Planet_has_been_attacked.append(planet)
                        break

    game.send_command_queue(commands)
    # next
# bye