import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
  meta: {
    skill_type: string;
  };
}

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  meta: {
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  uid: string;
  display_name: string;
  collections: {
    creatures: Creature[];
  };
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="flex flex-col h-full w-full bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between p-4">
        <div className="flex flex-col items-center">
          <PlayerCard
            uid={props.data.entities.player.uid}
            playerName={props.data.entities.player.display_name}
            imageUrl="/path/to/player/image.jpg"
            className="mb-4"
          />
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl={`/path/to/${playerCreature.meta.creature_type}_creature.jpg`}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
        <div className="flex space-x-4">
          <Shield className="text-blue-500" size={48} />
          <Swords className="text-red-500" size={48} />
        </div>
        <div className="flex flex-col items-center">
          <PlayerCard
            uid={props.data.entities.opponent.uid}
            playerName={props.data.entities.opponent.display_name}
            imageUrl="/path/to/opponent/image.jpg"
            className="mb-4"
          />
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl={`/path/to/${opponentCreature.meta.creature_type}_creature.jpg`}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-300">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
              disabled={!enabledUIDs.includes(skill.uid)}
              onClick={() => emitButtonClick(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
