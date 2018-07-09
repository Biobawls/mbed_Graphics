#include "mbed.h"
#include "npc_defines.h"
#include "npc_sprite.h"

bool assign_npc(uint8_t npc_type, npc_sprite* npc, uint32_t npc_ID, uint8_t vis_grid_x, uint8_t vis_grid_y, uint32_t loc, uint32_t world_x, uint32_t world_y, uint8_t ai, uint32_t update_rate) {
	bool success = true;
	switch (npc_type) {
		case 0: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, empty_sprite_array, empty_sprite_indexing, 28);
			break;
		}
		case 1: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, player_sprite_array, player_sprite_indexing, 28);
			break;
		}
		case 2: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, skeleman_sprite_array, skeleman_sprite_indexing, 28);
			break;
		}
		case 3: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, skelemage_sprite_array, skelemage_sprite_indexing, 28);
			break;
		}
		case 4: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, slimedood_sprite_array, slimedood_sprite_indexing, 28);
			break;
		}
		case 5: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, femalenpc2_sprite_array, femalenpc2_sprite_indexing, 28);
			break;
		}
		case 6: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, angryslime_sprite_array, angryslime_sprite_indexing, 28);
			break;
		}
		case 7: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, ratto_sprite_array, ratto_sprite_indexing, 28);
			break;
		}
		case 8: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, magidude_sprite_array, magidude_sprite_indexing, 28);
			break;
		}
		case 9: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, mage_sprite_array, mage_sprite_indexing, 28);
			break;
		}
		case 10: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, frogman_sprite_array, frogman_sprite_indexing, 28);
			break;
		}
		case 11: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, slimecat_sprite_array, slimecat_sprite_indexing, 28);
			break;
		}
		case 12: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, bandit_sprite_array, bandit_sprite_indexing, 28);
			break;
		}
		case 13: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, domo_sprite_array, domo_sprite_indexing, 28);
			break;
		}
		case 14: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, player2_sprite_array, player2_sprite_indexing, 28);
			break;
		}
		case 15: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, player3_sprite_array, player3_sprite_indexing, 28);
			break;
		}
		case 16: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, penguin_sprite_array, penguin_sprite_indexing, 28);
			break;
		}
		case 17: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, goblinvillagerM_sprite_array, goblinvillagerM_sprite_indexing, 28);
			break;
		}
		case 18: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, hobgoblinvillagerM_sprite_array, hobgoblinvillagerM_sprite_indexing, 28);
			break;
		}
		case 19: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, goblinguard_sprite_array, goblinguard_sprite_indexing, 28);
			break;
		}
		case 20: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, goblinflameguard_sprite_array, goblinflameguard_sprite_indexing, 28);
			break;
		}
		case 21: {
			npc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, malehumannpc_sprite_array, malehumannpc_sprite_indexing, 28);
			break;
		}
		default: {
			success = false;
			break;
		}
	}
	
	return success;
}
