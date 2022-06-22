import hlt
import logging
import random
from collections import OrderedDict
StartGame = hlt.Game("ZIZO")
logging.info("Starting my Faster bot!")

AOP = False  # Angriff auf besessene Planeten
Counter = 0

Angriff_starten = 120  # Starte den Angriff nach dieser Runde
StartMod1 = 150
StartMod2 = 10

def StatusCanBeUsed(Ship):
    if Ship.docking_status != Ship.DockingStatus.UNDOCKED:
        return True
    return False


def AddToPlanteAT(EntityShipOrPlanet):
    if isinstance(EntityShipOrPlanet[1][0], hlt.entity.Planet) and (not EntityShipOrPlanet[1][0].is_owned() or AOP):
        return True
    return False


def SetMode(PlanteAT , AOP  ):
    if not AOP and len(PlanteAT) == 0 or Counter > StartMod1:
        return True
    elif not AOP and Counter < StartMod2:
        return True
    elif AOP and Counter < StartMod2 and Counter > StartMod1:
        return False
   


while True:

    Map = StartGame.update_map()
    Befehle_Spiele = []
    PHBA = []  # Planet wurde angegriffen
    logging.info("Counter: " + str(Counter))
    Mapall_ships = Map.get_me().all_ships()
    listofplantdock = []
    for Ship in Mapall_ships:
        if StatusCanBeUsed(Ship):
            continue
        nearby_entities_by_distance_alles = Map.nearby_entities_by_distance(
            Ship)

        nearby_entities_by_distance_alles = sorted(nearby_entities_by_distance_alles.items(
        ), key=lambda e: e[0], reverse=False)

        PlanteAT = []
        Target = []
        for near in nearby_entities_by_distance_alles:
            if (AddToPlanteAT(near)):
                PlanteAT.append(near[1][0])

        AOP =  SetMode(PlanteAT , AOP)

        for planet in PlanteAT:
            if Ship.can_dock(planet) and (not planet.is_owned() or planet.owner.id != Map.my_id) and not planet in listofplantdock:
                if AOP:
                    listofplantdock.append(planet)
                Befehle_Spiele .append(Ship.dock(planet))
                break

            elif (Ship.can_dock(planet) and planet.is_owned() and planet.owner.id == Map.my_id and not planet.is_full()):
                Befehle_Spiele .append(Ship.dock(planet))
                break
            else:
                if planet in PHBA and not AOP:
                    continue
                else:
                    if not planet.is_owned() or planet.owner.id != Map.my_id:
                        if planet.is_owned():
                            xy = Ship.closest_point_to(
                                planet.all_docked_ships()[0])
                        else:
                            xy = Ship.closest_point_to(planet)
                            xy.x += random.randint(0, 10)*0.05
                            xy.y += random.randint(0, 10)*0.05
                        navigate_command = Ship.navigate(
                            xy,
                            Map,
                            speed=int(7),
                            ignore_ships=False)
                    else:
                        continue
                    if navigate_command:
                        Befehle_Spiele .append(navigate_command)
                        PHBA.append(planet)

                        break
    Counter += 1
    StartGame.send_command_queue(Befehle_Spiele)
