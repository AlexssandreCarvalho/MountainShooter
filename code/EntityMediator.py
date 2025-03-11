from code.Const import WIN_WIDTH
from code.Enemy import Enemy
from code.EnemyShot import EnemyShot
from code.Entity import Entity
from code.Player import Player
from code.PlayerShot import PlayerShot


class EntityMediator:

    @staticmethod
    def __verify_collision_window(ent: Entity):
        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:
                ent.health = 0

        if isinstance(ent, PlayerShot):
            if ent.rect.left >= WIN_WIDTH:
                ent.health = 0

        if isinstance(ent, EnemyShot):
            if ent.rect.right <= 0:
                ent.health = 0

    @staticmethod
    def __verify_collision_entity(ent_1, ent_2):
        # Auxiliary variable (flag) initialized to False
        valid_interaction = False

        # Enemy ship collisions and gunfire. We do not consider ship collisions or friendly fire
        if isinstance(ent_1, Enemy) and isinstance(ent_2, PlayerShot):
            valid_interaction = True

        elif isinstance(ent_1, PlayerShot) and isinstance(ent_2, Enemy):
            valid_interaction = True

        elif isinstance(ent_1, Player) and isinstance(ent_2, EnemyShot):
            valid_interaction = True

        elif isinstance(ent_1, EnemyShot) and isinstance(ent_2, Player):
            valid_interaction = True

        # Comparison for collisions between entities
        if valid_interaction:  # valid_interaction == True
            if (
                    ent_1.rect.right >= ent_2.rect.left and
                    ent_1.rect.left <= ent_2.rect.right and
                    ent_1.rect.bottom >= ent_2.rect.top and
                    ent_1.rect.top <= ent_2.rect.bottom
            ):
                # Last damage recorded for the Score
                ent_1.health -= ent_2.damage
                ent_2.health -= ent_1.damage
                ent_1.last_damage = ent_2.name
                ent_2.last_damage = ent_1.name

    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        if enemy.last_damage == 'Player1Shot':
            for ent in entity_list:
                if ent.name == 'Player1':
                    ent.score += enemy.score

        elif enemy.last_damage == 'Player2Shot':
            for ent in entity_list:
                if ent.name == 'Player2':
                    ent.score += enemy.score

    @staticmethod
    def verify_collision(entity_list: list[Entity]):

        for i in range(len(entity_list)):
            entity_1 = entity_list[i]
            EntityMediator.__verify_collision_window(entity_1)

            for j in range(i + 1, len(entity_list)):
                entity_2 = entity_list[j]
                EntityMediator.__verify_collision_entity(entity_1, entity_2)

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        for ent in entity_list:
            if ent.health <= 0:
                if isinstance(ent, Enemy):
                    EntityMediator.__give_score(ent, entity_list)
                entity_list.remove(ent)
