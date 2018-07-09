struct map004_struct {
	const static uint32_t world_y = 50;
	const static uint32_t world_x = 34;
	const static uint32_t world_n = 1700;

	const static uint8_t map[];
	const static uint8_t collision[];
	const static bool spawns[];

	const static uint32_t npc_n = 0;
	const static uint8_t npc_LUT[];
	const static uint8_t npc_move[];
	static const std::string npc_text[];
	const static uint32_t npc_pos[];
};
