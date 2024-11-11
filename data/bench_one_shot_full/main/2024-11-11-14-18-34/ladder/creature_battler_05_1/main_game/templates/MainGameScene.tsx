import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Button } from "@/components/ui/button";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
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
  __type: "Creature";
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

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  entities: {
    active_creature?: Creature;
  };
}

interface GameUIData {
  entities: {
    player: Player;
    bot: Player;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player?.entities.active_creature;
  const botCreature = props.data.entities.bot?.entities.active_creature;
  const player = props.data.entities.player;
  const bot = props.data.entities.bot;

  const handleSkillClick = () => {
    if (availableButtonSlugs.includes('attack')) {
      emitButtonClick('attack');
    }
  };

  const handleSwapClick = () => {
    if (availableButtonSlugs.includes('swap')) {
      emitButtonClick('swap');
    }
  };

  return (
    <div className="w-full h-full flex flex-col bg-gradient-to-b from-blue-100 to-blue-200">
      {/* Battlefield Area */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 p-4 gap-4">
        {/* Top Left - Bot Status */}
        <div className="flex items-center justify-center">
          {bot && botCreature && (
            <PlayerCard
              uid={bot.uid}
              name={bot.display_name}
              imageUrl="/placeholder/opponent.png"
            />
          )}
        </div>

        {/* Top Right - Bot Creature */}
        <div className="flex items-center justify-center">
          {botCreature && (
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              imageUrl="/placeholder/creature.png"
              currentHp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-center justify-center">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl="/placeholder/creature.png"
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex items-center justify-center">
          {player && playerCreature && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl="/placeholder/player.png"
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 p-4 bg-white/80">
        <div className="grid grid-cols-2 gap-4">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage,
                type: skill.meta.skill_type
              }}
              onClick={handleSkillClick}
            />
          ))}
          {availableButtonSlugs.includes('swap') && (
            <Button
              onClick={handleSwapClick}
              variant="secondary"
              className="w-full h-full"
            >
              Swap Creature
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
