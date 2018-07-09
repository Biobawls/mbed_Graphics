#include "mbed.h"
#include "items.h"
#include "effects.h"

////////////////////////////////////////////////////////////////////////////////
void items::init(char* item_name_in, const uint16_t *sa_in, uint8_t attack_in, uint8_t attrib_in, uint8_t skill_assign_in, uint8_t a_pix, bool use_in, bool equip_in) {
	uint8_t i_8;
	
	sprite_array = sa_in;
	alpha_channel = a_pix;
	attribute = attrib_in;
	skill_assign = skill_assign_in;
	stats.attack = attack_in;
	can_use = use_in;
	can_equip = equip_in;
	
	for (i_8 = 0; i_8 < item_name_char_limit-1; i_8++) {
		item_name[i_8] = item_name_in[i_8];
	}
	item_name[item_name_char_limit-1] = 0;
	
	return;
}
////////////////////////////////////////////////////////////////////////////////
bool assign_item(uint8_t choice, items* container) {
	bool success = true;
	
	switch (choice) {
		case 1: {
			container->init("RUSTY DGR ", rusty_dagger_sprite_array, 1, 0, 0, 28, false, true);
			break;
		}
		case 2: {
			container->init("COPPER DGR", copper_dagger_sprite_array, 2, 0, 0, 28, false, true);
			break;
		}
		case 3: {
			container->init("IRON DGR  ", iron_dagger_sprite_array, 3, 0, 0, 28, false, true);
			break;
		}
		case 4: {
			container->init("SILVER DGR", silver_dagger_sprite_array, 4, 0, 0, 28, false, true);
			break;
		}
		case 5: {
			container->init("GOLD DGR  ", gold_dagger_sprite_array, 5, 0, 0, 28, false, true);
			break;
		}
		case 6: {
			container->init("SELFHEAL  ", NULL, 1, 2, 4, 28, true, false);
			break;
		}
		case 7: {
			container->init("RUSTY SPR ", rusty_spear_sprite_array, 1, 0, 1, 28, true, false);
			break;
		}
		default: {
			success = false;
			break;
		}
	}
	
	return success;
}
