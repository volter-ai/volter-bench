import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, RefreshCw } from 'lucide-react'
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { Button } from "@/components/ui/button";

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  __type: "Creature";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  entities: {
    active_creature: Creature;
  };
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;

  const getCreatureImageUrl = (name: string) => `/creatures/${name.toLowerCase()}.png`;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="row-start-1 col-start-1 flex justify-start items-start">
          <CreatureCard
            uid={opponent.entities.active_creature?.uid ?? ""}
            name={opponent.entities.active_creature?.display_name ?? "Unknown"}
            image={getCreatureImageUrl(opponent.entities.active_creature?.display_name ?? "unknown")}
            hp={opponent.entities.active_creature?.stats.hp ?? 0}
            maxHp={opponent.entities.active_creature?.stats.max_hp ?? 1}
          />
        </div>

        {/* Opponent Creature */}
        <div className="row-start-1 col-start-2 flex justify-end items-start">
          <img 
            src={getCreatureImageUrl(opponent.entities.active_creature?.display_name ?? "unknown")} 
            alt="Opponent Creature" 
            className="w-40 h-40 object-contain"
          />
        </div>

        {/* Player Creature */}
        <div className="row-start-2 col-start-1 flex justify-start items-end">
          <img 
            src={getCreatureImageUrl(player.entities.active_creature?.display_name ?? "unknown")} 
            alt="Player Creature" 
            className="w-40 h-40 object-contain"
          />
        </div>

        {/* Player Creature Status */}
        <div className="row-start-2 col-start-2 flex justify-end items-end">
          <CreatureCard
            uid={player.entities.active_creature?.uid ?? ""}
            name={player.entities.active_creature?.display_name ?? "Unknown"}
            image={getCreatureImageUrl(player.entities.active_creature?.display_name ?? "unknown")}
            hp={player.entities.active_creature?.stats.hp ?? 0}
            maxHp={player.entities.active_creature?.stats.max_hp ?? 1}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4">
          {availableButtonSlugs.includes('attack') && (
            <Button onClick={() => emitButtonClick('attack')}>
              <Sword className="mr-2 h-4 w-4" /> Attack
            </Button>
          )}
          {availableButtonSlugs.includes('swap') && (
            <Button onClick={() => emitButtonClick('swap')}>
              <RefreshCw className="mr-2 h-4 w-4" /> Swap
            </Button>
          )}
          {player.entities.active_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Base Damage: ${skill.stats.base_damage}`}
              onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
            />
          ))}
        </div>
        <div className="mt-4 flex justify-between">
          <PlayerCard
            uid={player.uid}
            playerName={player.display_name}
            imageUrl={`/players/${player.display_name.toLowerCase().replace(' ', '_')}.png`}
          />
          <PlayerCard
            uid={opponent.uid}
            playerName={opponent.display_name}
            imageUrl={`/players/${opponent.display_name.toLowerCase().replace(' ', '_')}.png`}
          />
        </div>
      </div>
    </div>
  )
}
