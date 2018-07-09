#include "mbed.h"
#include "obj_defines.h"
#include "obj_sprite.h"

bool assign_obj(uint8_t obj_type, obj_sprite* obj, uint32_t obj_ID, uint8_t vis_grid_x, uint8_t vis_grid_y, uint32_t loc, uint32_t world_x, uint32_t world_y, bool colli_in, bool render_ontop_in) {
	bool success = true;
	switch (obj_type) {
		case 1: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, emptyobj_sprite_array, emptyobj_sprite_indexing, 28);
			break;
		}
		case 2: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, pot_sprite_array, pot_sprite_indexing, 28);
			break;
		}
		case 3: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, chairL_sprite_array, chairL_sprite_indexing, 28);
			break;
		}
		case 4: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, chairR_sprite_array, chairR_sprite_indexing, 28);
			break;
		}
		case 5: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, tableS_sprite_array, tableS_sprite_indexing, 28);
			break;
		}
		case 6: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, firewall_sprite_array, firewall_sprite_indexing, 28);
			break;
		}
		case 7: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, iceprison_sprite_array, iceprison_sprite_indexing, 28);
			break;
		}
		case 8: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, lava_sprite_array, lava_sprite_indexing, 28);
			break;
		}
		case 9: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, chestclosed_sprite_array, chestclosed_sprite_indexing, 28);
			break;
		}
		case 10: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, chestopen_sprite_array, chestopen_sprite_indexing, 28);
			break;
		}
		case 11: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, carpetTL_sprite_array, carpetTL_sprite_indexing, 28);
			break;
		}
		case 12: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, carpetT_sprite_array, carpetT_sprite_indexing, 28);
			break;
		}
		case 13: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, carpetTR_sprite_array, carpetTR_sprite_indexing, 28);
			break;
		}
		case 14: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, carpetML_sprite_array, carpetML_sprite_indexing, 28);
			break;
		}
		case 15: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, carpetM_sprite_array, carpetM_sprite_indexing, 28);
			break;
		}
		case 16: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, carpetMR_sprite_array, carpetMR_sprite_indexing, 28);
			break;
		}
		case 17: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, carpetBL_sprite_array, carpetBL_sprite_indexing, 28);
			break;
		}
		case 18: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, carpetB_sprite_array, carpetB_sprite_indexing, 28);
			break;
		}
		case 19: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, carpetBR_sprite_array, carpetBR_sprite_indexing, 28);
			break;
		}
		case 20: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, tableLL_sprite_array, tableLL_sprite_indexing, 28);
			break;
		}
		case 21: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, tableLR_sprite_array, tableLR_sprite_indexing, 28);
			break;
		}
		case 22: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, pottedplant_sprite_array, pottedplant_sprite_indexing, 28);
			break;
		}
		case 23: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, bookshelfB_sprite_array, bookshelfB_sprite_indexing, 28);
			break;
		}
		case 24: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, bookshelfT_sprite_array, bookshelfT_sprite_indexing, 28);
			break;
		}
		case 25: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, sofaSR_sprite_array, sofaSR_sprite_indexing, 28);
			break;
		}
		case 26: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, sofaSL_sprite_array, sofaSL_sprite_indexing, 28);
			break;
		}
		case 27: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, softchairR_sprite_array, softchairR_sprite_indexing, 28);
			break;
		}
		case 28: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, softchairG_sprite_array, softchairG_sprite_indexing, 28);
			break;
		}
		case 29: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, shield_sprite_array, shield_sprite_indexing, 28);
			break;
		}
		case 30: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, singlecandlelit_sprite_array, singlecandlelit_sprite_indexing, 28);
			break;
		}
		case 31: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, singlecandleunlit_sprite_array, singlecandleunlit_sprite_indexing, 28);
			break;
		}
		case 32: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, threecandlelit_sprite_array, threecandlelit_sprite_indexing, 28);
			break;
		}
		case 33: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, threecandleunlit_sprite_array, threecandleunlit_sprite_indexing, 28);
			break;
		}
		case 34: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, threebluecandlelit_sprite_array, threebluecandlelit_sprite_indexing, 28);
			break;
		}
		case 35: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, threesilvercandlelit_sprite_array, threesilvercandlelit_sprite_indexing, 28);
			break;
		}
		case 36: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, threesilvercandleunlit_sprite_array, threesilvercandleunlit_sprite_indexing, 28);
			break;
		}
		case 37: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, wallsilvercandlelit_sprite_array, wallsilvercandlelit_sprite_indexing, 28);
			break;
		}
		case 38: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, wallsilvercandleunlit_sprite_array, wallsilvercandleunlit_sprite_indexing, 28);
			break;
		}
		case 39: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, wallcandlelit_sprite_array, wallcandlelit_sprite_indexing, 28);
			break;
		}
		case 40: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, wallcandleunlit_sprite_array, wallcandleunlit_sprite_indexing, 28);
			break;
		}
		case 41: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, wallshieldcandlelit_sprite_array, wallshieldcandlelit_sprite_indexing, 28);
			break;
		}
		case 42: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, wallshieldcandleunlit_sprite_array, wallshieldcandleunlit_sprite_indexing, 28);
			break;
		}
		case 43: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, redbedT_sprite_array, redbedT_sprite_indexing, 28);
			break;
		}
		case 44: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, redbedB_sprite_array, redbedB_sprite_indexing, 28);
			break;
		}
		case 45: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, smallwindow_sprite_array, smallwindow_sprite_indexing, 28);
			break;
		}
		case 46: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, boiler_sprite_array, boiler_sprite_indexing, 28);
			break;
		}
		case 47: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, cabinet_sprite_array, cabinet_sprite_indexing, 28);
			break;
		}
		case 48: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, emptydesk_sprite_array, emptydesk_sprite_indexing, 28);
			break;
		}
		case 49: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, inkwelldesk_sprite_array, inkwelldesk_sprite_indexing, 28);
			break;
		}
		case 50: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, greenpotdesk_sprite_array, greenpotdesk_sprite_indexing, 28);
			break;
		}
		case 51: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, redpotdesk_sprite_array, redpotdesk_sprite_indexing, 28);
			break;
		}
		case 52: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, alchdesk_sprite_array, alchdesk_sprite_indexing, 28);
			break;
		}
		case 53: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, writedesk_sprite_array, writedesk_sprite_indexing, 28);
			break;
		}
		case 54: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, furnace_sprite_array, furnace_sprite_indexing, 28);
			break;
		}
		case 55: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, bluebedtop_sprite_array, bluebedtop_sprite_indexing, 28);
			break;
		}
		case 56: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, bluebedbottom_sprite_array, bluebedbottom_sprite_indexing, 28);
			break;
		}
		case 57: {
			obj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, firevortex_sprite_array, firevortex_sprite_indexing, 28);
			break;
		}
		default: {
			success = false;
			break;
		}
	}
	if (colli_in == true) {
		obj->enable_collision();
	} else {
		obj->disable_collision();
	}
	if (render_ontop_in == true) {
		obj->render_top();
	} else {
		obj->render_bottom();
	}
	
	return success;
}
