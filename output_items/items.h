#ifndef ITEMS_H
#define ITEMS_H

#include "mbed.h"

////////////////////////////////////////////////////////////////////////////////
// sprite index in ROM
////////////////////////////////////////////////////////////////////////////////
const static uint16_t rusty_dagger_sprite_array[1] = {252};
const static uint16_t copper_dagger_sprite_array[1] = {253};
const static uint16_t iron_dagger_sprite_array[1] = {254};
const static uint16_t silver_dagger_sprite_array[1] = {255};
const static uint16_t gold_dagger_sprite_array[1] = {256};
const static uint16_t rusty_spear_sprite_array[1] = {275};

class items {
	public:
		items(void){
			uint8_t i_8 = 0;
			
			sprite_array = NULL;
			
			attribute = 0;
			stats.attack = 1;
			skill_assign = 255;
			
			can_use = false;
			can_equip = false;
			
			for (i_8 = 0; i_8 < item_name_char_limit; i_8++) {
				item_name[i_8] = 0;
			}
			
			return;
		};
		
		void init(char* item_name_in, const uint16_t *sa_in, uint8_t attack_in, uint8_t attrib_in, uint8_t skill_assign_in, uint8_t a_pix, bool use_in, bool equip_in);
		
		const uint16_t *sprite_array;
		uint8_t alpha_channel;
		
		// attribute numbers: 0 = physical, 1 = fire, 2 = ice, 3 = arcane, 4 = nature, 5 = light, 6 = dark
		uint8_t attribute;
		
		uint8_t skill_assign;
		
		static const uint8_t item_name_char_limit = 11;
		char item_name[item_name_char_limit];
		
		struct stats_struct {
			// Combat
			int16_t attack;
		} stats;
		
		bool can_use;
		bool can_equip;
};

bool assign_item(uint8_t choice, items* container);

#endif
