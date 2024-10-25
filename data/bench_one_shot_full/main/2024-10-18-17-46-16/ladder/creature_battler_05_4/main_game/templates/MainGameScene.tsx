import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  uid: string;
  display_name: string;
  entities: {
    active_creature: Creature;
  };
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;

  const renderSkillButtons = () => {
    const buttons = [];

    if (availableButtonSlugs.includes('attack')) {
      buttons.push(
        <SkillButton
          key="attack"
          uid="attack"
          skillName="Attack"
          description="Choose an attack"
          stats=""
          onClick={() => emitButtonClick('attack')}
        >
          <Sword className="mr-2 h-4 w-4" /> Attack
        </SkillButton>
      );
    }

    if (availableButtonSlugs.includes('swap')) {
      buttons.push(
        <SkillButton
          key="swap"
          uid="swap"
          skillName="Swap"
          description="Swap creatures"
          stats=""
          onClick={() => emitButtonClick('swap')}
        >
          <Repeat className="mr-2 h-4 w-4" /> Swap
        </SkillButton>
      );
    }

    player.entities.active_creature?.collections.skills.forEach((skill) => {
      if (availableButtonSlugs.includes(skill.uid)) {
        buttons.push(
          <SkillButton
            key={skill.uid}
            uid={skill.uid}
            skillName={skill.display_name}
            description={skill.description}
            stats={`Damage: ${skill.stats.base_damage}`}
            onClick={() => emitButtonClick(skill.uid)}
          />
        );
      }
    });

    // Ensure we have a 2x2 grid by adding empty buttons if necessary
    while (buttons.length < 4) {
      buttons.push(<div key={`empty-${buttons.length}`} />);
    }

    return buttons;
  };

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-7xl aspect-video bg-white shadow-lg rounded-lg overflow-hidden">
        <div className="h-2/3 grid grid-cols-2 grid-rows-2 p-4 gap-4">
          <div className="row-start-2 col-start-1 flex items-end justify-start">
            <CreatureCard
              uid={player.entities.active_creature?.uid || ''}
              name={player.entities.active_creature?.display_name || 'Unknown'}
              image={`/creatures/${player.entities.active_creature?.uid || 'default'}_back.png`}
              hp={player.entities.active_creature?.stats.hp || 0}
              maxHp={player.entities.active_creature?.stats.max_hp || 1}
            />
          </div>
          <div className="row-start-2 col-start-2 flex items-end justify-end">
            <div>
              <h3>{player.entities.active_creature?.display_name || 'Unknown'}</h3>
              <div>HP: {player.entities.active_creature?.stats.hp}/{player.entities.active_creature?.stats.max_hp}</div>
            </div>
          </div>
          <div className="row-start-1 col-start-2 flex items-start justify-end">
            <CreatureCard
              uid={opponent.entities.active_creature?.uid || ''}
              name={opponent.entities.active_creature?.display_name || 'Unknown'}
              image={`/creatures/${opponent.entities.active_creature?.uid || 'default'}_front.png`}
              hp={opponent.entities.active_creature?.stats.hp || 0}
              maxHp={opponent.entities.active_creature?.stats.max_hp || 1}
            />
          </div>
          <div className="row-start-1 col-start-1 flex items-start justify-start">
            <div>
              <h3>{opponent.entities.active_creature?.display_name || 'Unknown'}</h3>
              <div>HP: {opponent.entities.active_creature?.stats.hp}/{opponent.entities.active_creature?.stats.max_hp}</div>
            </div>
          </div>
        </div>
        <div className="h-1/3 p-4">
          <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
            {renderSkillButtons()}
          </div>
        </div>
      </div>
    </div>
  );
}
