#ifndef NPC_DEFINES_H
#define NPC_DEFINES_H

#include "mbed.h"
#include "npc_sprite.h"

////////////////////////////////////////////////////////////////////////////////
// sprite index in ROM
////////////////////////////////////////////////////////////////////////////////
// 0 = left1, 1 = left2, 2 = right1, 3 = right2, 4 = up1, 5 = up2, 6 = down1, 7 = down2
const static uint16_t cursor_sprite_array[8] = {2, 2, 2, 2, 2, 2, 2, 2};
const static uint8_t cursor_sprite_indexing[8] = {0, 0, 0, 0, 0, 0, 0, 0};
const static uint16_t cursor_fill_sprite_array[8] = {4, 4, 4, 4, 4, 4, 4, 4};
const static uint8_t cursor_fill_sprite_indexing[8] = {0, 0, 0, 0, 0, 0, 0, 0};
const static uint16_t empty_sprite_array[8] = {7, 7, 7, 7, 7, 7, 7, 7};
const static uint8_t empty_sprite_indexing[8] = {0, 0, 0, 0, 0, 0, 0, 0};
const static uint16_t player_sprite_array[8] = {20, 21, 20, 21, 16, 17, 18, 19};
const static uint8_t player_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t skeleman_sprite_array[8] = {30, 31, 30, 31, 28, 29, 24, 25};
const static uint8_t skeleman_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t skelemage_sprite_array[8] = {34, 35, 34, 35, 32, 33, 26, 27};
const static uint8_t skelemage_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t slimedood_sprite_array[8] = {40, 41, 40, 41, 38, 39, 36, 37};
const static uint8_t slimedood_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t femalenpc2_sprite_array[8] = {49, 50, 49, 50, 47, 48, 45, 46};
const static uint8_t femalenpc2_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t angryslime_sprite_array[8] = {74, 75, 74, 75, 72, 73, 70, 71};
const static uint8_t angryslime_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t ratto_sprite_array[8] = {89, 90, 89, 90, 87, 88, 85, 86};
const static uint8_t ratto_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t magidude_sprite_array[8] = {105, 106, 105, 106, 103, 104, 101, 102};
const static uint8_t magidude_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t mage_sprite_array[8] = {111, 112, 111, 112, 109, 110, 107, 108};
const static uint8_t mage_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t frogman_sprite_array[8] = {117, 118, 117, 118, 115, 116, 113, 114};
const static uint8_t frogman_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t slimecat_sprite_array[8] = {136, 137, 136, 137, 134, 135, 132, 133};
const static uint8_t slimecat_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t bandit_sprite_array[8] = {155, 156, 155, 156, 153, 154, 151, 152};
const static uint8_t bandit_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t domo_sprite_array[8] = {173, 174, 173, 174, 130, 131, 128, 129};
const static uint8_t domo_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t player2_sprite_array[8] = {187, 188, 187, 188, 183, 184, 185, 186};
const static uint8_t player2_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t player3_sprite_array[8] = {193, 194, 193, 194, 191, 192, 189, 190};
const static uint8_t player3_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t penguin_sprite_array[8] = {219, 220, 219, 220, 217, 218, 215, 216};
const static uint8_t penguin_sprite_indexing[8] = {0, 0, 1, 1, 0, 0, 0, 0};
const static uint16_t goblinvillagerM_sprite_array[8] = {355, 356, 355, 356, 353, 354, 351, 352};
const static uint8_t goblinvillagerM_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t hobgoblinvillagerM_sprite_array[8] = {361, 362, 361, 362, 359, 360, 357, 358};
const static uint8_t hobgoblinvillagerM_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t goblinguard_sprite_array[8] = {367, 368, 367, 368, 365, 366, 363, 364};
const static uint8_t goblinguard_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t goblinflameguard_sprite_array[8] = {373, 374, 373, 374, 371, 372, 369, 370};
const static uint8_t goblinflameguard_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};
const static uint16_t malehumannpc_sprite_array[8] = {410, 411, 410, 411, 42, 43, 22, 23};
const static uint8_t malehumannpc_sprite_indexing[8] = {1, 1, 0, 0, 0, 0, 0, 0};

bool assign_npc(uint8_t npc_type, npc_sprite* npc, uint32_t npc_ID, uint8_t vis_grid_x, uint8_t vis_grid_y, uint32_t loc, uint32_t world_x, uint32_t world_y, uint8_t ai, uint32_t update_rate);

#endif
