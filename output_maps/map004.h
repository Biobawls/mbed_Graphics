struct map004_struct {
	const static uint32_t world_y = 50;
	const static uint32_t world_x = 34;
	const static uint32_t world_n = 1700;

	const static uint16_t map[];
	const static uint8_t collision[];
	const static bool spawns[];

	const static uint8_t npc_n = 0;
	const static uint8_t npc_LUT[];
	const static uint8_t npc_move[];
	static const std::string npc_text[];
	const static uint32_t npc_pos[];

	const static uint8_t obj_n = 0;
	const static uint8_t obj_LUT[];
	const static uint32_t obj_pos[];
	const static bool obj_colli[];

	const static uint8_t item_n = 0;
	const static uint8_t item_LUT[];
	const static uint32_t item_pos[];
	const static uint8_t item_in_list[];
};
