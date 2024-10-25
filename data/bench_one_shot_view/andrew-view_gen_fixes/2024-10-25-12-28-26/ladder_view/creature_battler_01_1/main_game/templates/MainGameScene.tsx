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
  description: string;
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

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2 flex justify-between items-center">
        <div className="flex items-center">
          <Shield className="mr-2" />
          <span>Player: {props.data.entities.player.display_name}</span>
        </div>
        <div className="flex items-center">
          <span>Opponent: {props.data.entities.foe.display_name}</span>
          <Swords className="ml-2" />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <span className="mb-2 text-lg font-bold">Player</span>
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl={`/creatures/${playerCreature.uid}.jpg`}
            hp={playerCreature.stats.hp}
          />
        </div>
        <div className="flex flex-col items-center">
          <span className="mb-2 text-lg font-bold">Opponent</span>
          <CreatureCard
            uid={foeCreature.uid}
            name={foeCreature.display_name}
            imageUrl={`/creatures/${foeCreature.uid}.jpg`}
            hp={foeCreature.stats.hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 h-1/3 overflow-y-auto flex flex-col justify-center items-center">
        {availableButtonSlugs.length > 0 ? (
          <>
            <div className="text-center text-lg mb-4">Choose a skill to use:</div>
            <div className="grid grid-cols-2 gap-4">
              {playerCreature.collections.skills.map((skill) => (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  skillName={skill.display_name}
                  description={skill.description}
                  stats={`Damage: ${skill.stats.damage}`}
                  onClick={() => availableButtonSlugs.includes(skill.uid) && emitButtonClick(skill.uid)}
                  disabled={!availableButtonSlugs.includes(skill.uid)}
                />
              ))}
            </div>
          </>
        ) : (
          <div className="text-center text-lg">
            Waiting for game action...
          </div>
        )}
      </div>
    </div>
  );
}
