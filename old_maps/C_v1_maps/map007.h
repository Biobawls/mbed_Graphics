struct map007_struct {
	const static uint32_t world_y = 15;
	const static uint32_t world_x = 15;
	const static uint32_t world_n = 225;

	const static uint8_t map[];
	const static uint8_t collision[];
	const static bool spawns[];

	const static uint32_t npc_n = 1;
	const static uint8_t npc_LUT[];
	const static uint8_t npc_move[];
	static const std::string npc_text[];
	const static uint32_t npc_pos[];
};
