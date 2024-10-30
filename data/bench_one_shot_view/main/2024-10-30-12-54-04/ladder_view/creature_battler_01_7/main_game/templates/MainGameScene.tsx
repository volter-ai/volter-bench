import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  stats: {
    damage: number;
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
  };
  uid: string;
  display_name: string;
  description: string;
  collections: {
    skills: Skill[];
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    foe: Player;
    player_creature: Creature;
    foe_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const foeCreature = props.data.entities.foe_creature;

  // Function to get a placeholder image URL if not provided in the data
  const getImageUrl = (creature: Creature | undefined) => {
    return creature?.meta?.imageUrl || "/placeholder-creature.jpg";
  };

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2 flex justify-between items-center">
        <div className="flex items-center">
          <Shield className="mr-2" />
          <span>Player: {props.data.entities.player?.display_name}</span>
        </div>
        <div className="flex items-center">
          <span>Opponent: {props.data.entities.foe?.display_name}</span>
          <Swords className="ml-2" />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <span className="mb-2 text-lg font-bold">Player</span>
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={getImageUrl(playerCreature)}
              hp={playerCreature.stats.hp}
            />
          )}
        </div>
        <div className="flex flex-col items-center">
          <span className="mb-2 text-lg font-bold">Opponent</span>
          {foeCreature && (
            <CreatureCard
              uid={foeCreature.uid}
              name={foeCreature.display_name}
              imageUrl={getImageUrl(foeCreature)}
              hp={foeCreature.stats.hp}
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-300">
        <div className="mb-4 h-24 overflow-y-auto bg-gray-100 p-2 rounded">
          {/* Game text would go here */}
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              onClick={() => emitButtonClick(skill.uid)}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
