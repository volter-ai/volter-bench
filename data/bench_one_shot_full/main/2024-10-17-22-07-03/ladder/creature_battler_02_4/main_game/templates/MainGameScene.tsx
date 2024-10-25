import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  stats: {
    base_damage: number;
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
    speed: number;
  };
  collections: {
    skills: Skill[];
  };
  uid: string;
  display_name: string;
}

interface Player {
  __type: "Player";
  collections: {
    creatures: Creature[];
  };
  uid: string;
  display_name: string;
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
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl="/placeholder-player-creature.png"
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            className="mb-2"
          />
          <div className="flex items-center">
            <Swords className="mr-1" /> {playerCreature.stats.attack}
            <Shield className="ml-2 mr-1" /> {playerCreature.stats.defense}
          </div>
        </div>
        <div className="text-4xl font-bold">VS</div>
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl="/placeholder-opponent-creature.png"
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            className="mb-2"
          />
          <div className="flex items-center">
            <Swords className="mr-1" /> {opponentCreature.stats.attack}
            <Shield className="ml-2 mr-1" /> {opponentCreature.stats.defense}
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-200">
        <div className="mb-4">
          <p className="text-lg">What will {playerCreature.display_name} do?</p>
        </div>
        <div className="grid grid-cols-2 gap-2">
          {playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              disabled={!enabledUIDs.includes(skill.uid)}
              onClick={() => emitButtonClick(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
