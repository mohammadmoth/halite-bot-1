import hlt
import logging
import random
from collections import OrderedDict
game = hlt.Game("Basic Bot2")
logging.info("Starting my Faster bot!")
ignore_planttacksame = False
AttackOwnerPlanet = False
while True:
    Map = game.update_map()
    commands = []
    Planet_has_been_attacked = []

    alltroops = Map.get_me().all_ships()

    for arrmy in alltroops:

        targetplanet = []
        targetarrmy = []

        if arrmy.docking_status != arrmy.DockingStatus.UNDOCKED:
            logging.info("id: " + str(arrmy.id) + " status: " +
                         str(arrmy.docking_status))
            continue


        entities_by_distance_all = Map.nearby_entities_by_distance(arrmy)

        entities_by_distance_all = sorted(
            entities_by_distance_all.items(), key=lambda entities_by_distance_allX: entities_by_distance_allX[0], reverse=False)

        for target in entities_by_distance_all:
            if isinstance(target[1][0], hlt.entity.Planet) and target[1][0].is_owned():
                logging.info(target[1][0].owner.id)
            if isinstance(target[1][0], hlt.entity.Planet) and (not target[1][0].is_owned() or AttackOwnerPlanet):
                targetplanet.append(target[1][0])

          #  else:
          #      logging.info()

       # logging.info(targetplanet)
       # logging.info(targetarrmy)
        logging.info(" Count Targets :" + str(len(targetplanet)))
        if len(targetplanet) == 0:
            AttackOwnerPlanet = True
            ignore_planttacksame = True
        for planet in targetplanet:
            if arrmy.can_dock(planet) and (not planet.is_owned() or planet.owner.id != Map.my_id):
                commands.append(arrmy.dock(planet))
                logging.info(" dock on planet :" +
                             str(planet.id) + " Ship :" + str(arrmy.id))
                break
            else:
                if planet in Planet_has_been_attacked and not ignore_planttacksame:
                    logging.info("Same Attack")
                    continue
                else:
                    if not planet.is_owned() or planet.owner.id != Map.my_id:
                        xy = arrmy.closest_point_to(planet)
                        navigate_command = arrmy.navigate(
                            xy,
                            Map,
                            speed=int(hlt.constants.MAX_SPEED),
                            ignore_ships=False)
                    else:
                        continue
                    if navigate_command:
                        commands.append(navigate_command)
                        Planet_has_been_attacked.append(planet)
                        logging.info(
                            " Attack on planet :" + str(planet.id) + " Ship :" + str(arrmy.id))
                        break
    game.send_command_queue(commands)
    # next
# bye