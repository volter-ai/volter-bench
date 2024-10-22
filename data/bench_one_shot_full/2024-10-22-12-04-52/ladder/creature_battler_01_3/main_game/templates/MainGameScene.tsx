import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const botCreature = props.data.entities.bot_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2 flex justify-between items-center">
        <div className="flex items-center">
          <Shield className="mr-2" />
          <span>Player</span>
        </div>
        <div className="flex items-center">
          <span>Opponent</span>
          <Swords className="ml-2" />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center p-4">
        <CreatureCard
          uid={playerCreature.uid}
          name={playerCreature.display_name}
          imageUrl="/path/to/player-creature-image.jpg"
          hp={playerCreature.stats.hp}
          maxHp={playerCreature.stats.max_hp}
        />
        <CreatureCard
          uid={botCreature.uid}
          name={botCreature.display_name}
          imageUrl="/path/to/bot-creature-image.jpg"
          hp={botCreature.stats.hp}
          maxHp={botCreature.stats.max_hp}
        />
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 h-1/3 overflow-y-auto">
        <div className="mb-2 text-center font-bold">Your turn!</div>
        {availableButtonSlugs.length > 0 ? (
          <div className="flex flex-wrap gap-2 justify-center">
            {availableButtonSlugs.map((slug) => {
              const skill = playerCreature.collections.skills.find(skill => skill.uid === slug);
              return skill ? (
                <SkillButton
                  key={slug}
                  uid={slug}
                  skillName={skill.display_name}
                  description={skill.description}
                  stats={`Damage: ${skill.stats.damage}`}
                  onClick={() => emitButtonClick(slug)}
                />
              ) : null;
            })}
          </div>
        ) : (
          <div className="text-lg text-center">
            Game text will be displayed here when no buttons are available.
          </div>
        )}
      </div>
    </div>
  );
}
