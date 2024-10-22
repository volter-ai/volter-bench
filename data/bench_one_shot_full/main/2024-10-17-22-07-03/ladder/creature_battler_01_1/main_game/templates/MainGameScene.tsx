import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Heart, Swords, RotateCcw, LogOut } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

interface Skill {
  __type: "Skill";
  stats: { [key: string]: number };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: { hp: number; max_hp: number };
  uid: string;
  display_name: string;
  description: string;
  collections: { skills: Skill[] };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  collections: { creatures: Creature[] };
}

interface GameUIData {
  entities: {
    player: Player;
    bot: Player;
    player_creature: Creature;
    bot_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const playerCreature = props.data.entities.player_creature;
  const botCreature = props.data.entities.bot_creature;

  return (
    <div className="w-full h-full aspect-video bg-gray-100 flex flex-col">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2 flex justify-between items-center">
        <div className="flex items-center">
          <Heart className="mr-2" />
          <span>Player HP: {playerCreature?.stats.hp ?? 0}/{playerCreature?.stats.max_hp ?? 0}</span>
        </div>
        <div className="flex items-center">
          <Swords className="mr-2" />
          <span>Battle in Progress</span>
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <CreatureCard
          uid={playerCreature?.uid ?? ""}
          name={playerCreature?.display_name ?? "Unknown"}
          imageUrl="/placeholder-creature.jpg"
          hp={playerCreature?.stats.hp ?? 0}
          className="transform scale-x-[-1]"
        />
        <CreatureCard
          uid={botCreature?.uid ?? ""}
          name={botCreature?.display_name ?? "Unknown"}
          imageUrl="/placeholder-creature.jpg"
          hp={botCreature?.stats.hp ?? 0}
        />
      </div>

      {/* User Interface */}
      <div className="bg-gray-200 p-4 h-1/3">
        <div className="bg-white rounded-lg p-4 h-full flex flex-col">
          <div className="flex-grow overflow-y-auto mb-4">
            {/* Game text would go here */}
          </div>
          <div className="flex flex-wrap gap-2">
            {playerCreature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={Object.entries(skill.stats).map(([key, value]) => `${key}: ${value}`).join(', ')}
                disabled={!enabledUIDs.includes(skill.uid)}
              />
            ))}
            {availableButtonSlugs.includes('play-again') && (
              <Button onClick={() => emitButtonClick('play-again')}>
                <RotateCcw className="mr-2" />
                Play Again
              </Button>
            )}
            {availableButtonSlugs.includes('quit') && (
              <Button onClick={() => emitButtonClick('quit')}>
                <LogOut className="mr-2" />
                Quit
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
