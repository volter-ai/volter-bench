import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { Button } from "@/components/ui/button";

interface Skill {
  __type: "Skill";
  stats: {
    base_damage: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    skill_type: string;
    is_physical: boolean;
  };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    sp_attack: number;
    sp_defense: number;
    speed: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
  uid: string;
  display_name: string;
  description: string;
}

interface Player {
  __type: "Player";
  meta: {
    prototype_id: string;
    category: string;
  };
  collections: {
    creatures: Creature[];
  };
  uid: string;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-0 pb-[56.25%] relative">
      <div className="absolute inset-0 flex flex-col">
        {/* Battlefield */}
        <div className="flex-grow flex">
          {/* Opponent */}
          <div className="w-1/2 flex flex-col">
            <div className="flex-grow flex items-start justify-end p-4">
              <CreatureCard
                uid={opponent_creature.uid}
                name={opponent_creature.display_name}
                image={`/images/creatures/${opponent_creature.meta.prototype_id}_front.png`}
                hp={opponent_creature.stats.hp}
                maxHp={opponent_creature.stats.max_hp}
              />
            </div>
            <div className="h-1/3 flex items-end justify-start p-4">
              <PlayerCard
                uid={opponent.uid}
                playerName={opponent.display_name}
                imageUrl={`/images/players/${opponent.meta.prototype_id}.png`}
              />
            </div>
          </div>
          {/* Player */}
          <div className="w-1/2 flex flex-col">
            <div className="h-1/3 flex items-start justify-end p-4">
              <PlayerCard
                uid={player.uid}
                playerName={player.display_name}
                imageUrl={`/images/players/${player.meta.prototype_id}.png`}
              />
            </div>
            <div className="flex-grow flex items-end justify-start p-4">
              <CreatureCard
                uid={player_creature.uid}
                name={player_creature.display_name}
                image={`/images/creatures/${player_creature.meta.prototype_id}_back.png`}
                hp={player_creature.stats.hp}
                maxHp={player_creature.stats.max_hp}
              />
            </div>
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 bg-gray-100 p-4">
          <div className="grid grid-cols-2 gap-4 h-full">
            {player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}`}
                disabled={!availableButtonSlugs.includes(skill.uid)}
              />
            ))}
            {availableButtonSlugs.includes('play-again') && (
              <Button onClick={() => emitButtonClick('play-again')}>
                <Play className="mr-2 h-4 w-4" /> Play Again
              </Button>
            )}
            {availableButtonSlugs.includes('quit') && (
              <Button onClick={() => emitButtonClick('quit')} variant="destructive">
                <X className="mr-2 h-4 w-4" /> Quit
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
