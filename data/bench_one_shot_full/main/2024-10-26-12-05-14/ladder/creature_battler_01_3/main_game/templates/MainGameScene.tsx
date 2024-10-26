import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Button } from "@/components/ui/button";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { User, UserMinus } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
  };
}

interface GameUIData {
  entities: {
    player_creature: Creature;
    bot_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const botCreature = props.data.entities.bot_creature;

  return (
    <div className="w-full h-full aspect-video bg-gray-100 flex flex-col">
      {/* HUD */}
      <nav className="bg-blue-500 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <User className="mb-2" />
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl="/placeholder-player-creature.jpg"
            hp={playerCreature.stats.hp}
          />
        </div>
        <div className="flex flex-col items-center">
          <UserMinus className="mb-2" />
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            imageUrl="/placeholder-bot-creature.jpg"
            hp={botCreature.stats.hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-gray-200 p-4 h-1/3 flex flex-col justify-between">
        {availableButtonSlugs.includes('use-skill') && playerCreature.collections.skills.length > 0 ? (
          <div className="flex-grow border border-gray-300 p-2 mb-2 grid grid-cols-2 gap-2">
            {playerCreature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                onClick={() => emitButtonClick('use-skill', { skillId: skill.uid })}
              />
            ))}
          </div>
        ) : (
          <div className="flex-grow border border-gray-300 p-2 mb-2 text-center">
            <p className="text-lg">A wild creature appears!</p>
          </div>
        )}
        {availableButtonSlugs.includes('quit') && (
          <Button
            className="w-full mt-2"
            onClick={() => emitButtonClick('quit')}
          >
            Quit
          </Button>
        )}
      </div>
    </div>
  );
}
