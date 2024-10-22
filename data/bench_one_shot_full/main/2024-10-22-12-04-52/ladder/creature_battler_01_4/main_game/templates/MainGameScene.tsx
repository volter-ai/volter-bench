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
    bot: Player;
    player_creature: Creature;
    bot_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const botCreature = props.data.entities.bot_creature;

  return (
    <div className="w-full h-full flex flex-col">
      {/* HUD */}
      <nav className="w-full h-16 bg-gray-800 text-white flex items-center justify-between px-4">
        <div>Player: {props.data.entities.player.display_name}</div>
        <div>Opponent: {props.data.entities.bot.display_name}</div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center px-8">
        <div className="flex flex-col items-center">
          <Shield className="w-8 h-8 mb-2" />
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl="/placeholder-creature.jpg"
            hp={playerCreature.stats.hp}
          />
        </div>
        <div className="flex flex-col items-center">
          <Swords className="w-8 h-8 mb-2" />
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            imageUrl="/placeholder-creature.jpg"
            hp={botCreature.stats.hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="w-full h-1/3 bg-gray-100 p-4 overflow-y-auto">
        <div className="flex flex-wrap gap-2">
          {playerCreature.collections.skills.map((skill) => {
            const isAvailable = availableButtonSlugs.includes(skill.uid);
            return (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                onClick={() => isAvailable && emitButtonClick(skill.uid)}
                disabled={!isAvailable}
              />
            );
          })}
        </div>
        {playerCreature.collections.skills.length === 0 && (
          <div className="text-center">
            No skills available
          </div>
        )}
      </div>
    </div>
  );
}
