struct test_struct {
	const static uint32_t world_y = 20;
	const static uint32_t world_x = 20;
	const static uint32_t world_n = 400;

	const static uint16_t map[];
	const static uint8_t collision[];
	const static bool spawns[];

	const static uint8_t npc_n = 1;
	const static uint8_t npc_LUT[];
	const static uint8_t npc_move[];
	static const std::string npc_text[];
	const static uint32_t npc_pos[];

	const static uint8_t obj_n = 1;
	const static uint8_t obj_LUT[];
	const static uint32_t obj_pos[];
	const static bool obj_colli[];

	const static uint8_t item_n = 5;
	const static uint8_t item_LUT[];
	const static uint32_t item_pos[];
	const static uint8_t item_in_list[];
};
