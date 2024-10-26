import { useCurrentButtons } from "@/lib/useChoices.ts";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";
import { Shield, Swords, Zap } from 'lucide-react';

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
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const renderCreature = (creature: Creature, isPlayer: boolean) => (
    <div className={`flex flex-col items-center ${isPlayer ? 'order-1' : 'order-2'}`}>
      <CreatureCard
        uid={creature.uid}
        name={creature.display_name}
        imageUrl={`/images/creatures/${creature.uid}.png`}
        hp={creature.stats.hp}
        maxHp={creature.stats.max_hp}
      />
      <div className="mt-2 flex space-x-2">
        <div className="flex items-center">
          <Swords className="w-4 h-4 mr-1" />
          <span>{creature.stats.attack}</span>
        </div>
        <div className="flex items-center">
          <Shield className="w-4 h-4 mr-1" />
          <span>{creature.stats.defense}</span>
        </div>
        <div className="flex items-center">
          <Zap className="w-4 h-4 mr-1" />
          <span>{creature.stats.speed}</span>
        </div>
      </div>
    </div>
  );

  const renderSkillButtons = (skills: Skill[]) => (
    <div className="flex flex-wrap justify-center gap-2 mt-4">
      {skills.map((skill) => (
        <SkillButton
          key={skill.uid}
          uid={skill.uid}
          skillName={skill.display_name}
          description={skill.description}
          stats={`Damage: ${skill.stats.base_damage}`}
          onClick={() => emitButtonClick(skill.uid)}
        />
      ))}
    </div>
  );

  const renderActionButtons = () => (
    <div className="flex justify-center space-x-4 mt-4">
      {availableButtonSlugs.includes('play-again') && (
        <Button onClick={() => emitButtonClick('play-again')}>Play Again</Button>
      )}
      {availableButtonSlugs.includes('quit') && (
        <Button onClick={() => emitButtonClick('quit')}>Quit</Button>
      )}
    </div>
  );

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <PlayerCard
          uid={props.data.entities.player.uid}
          playerName={props.data.entities.player.display_name}
          imageUrl={`/images/players/${props.data.entities.player.uid}.png`}
        />
        <h1 className="text-2xl font-bold">Battle Arena</h1>
        <PlayerCard
          uid={props.data.entities.opponent.uid}
          playerName={props.data.entities.opponent.display_name}
          imageUrl={`/images/players/${props.data.entities.opponent.uid}.png`}
        />
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-around items-center p-4">
        {renderCreature(props.data.entities.player_creature, true)}
        {renderCreature(props.data.entities.opponent_creature, false)}
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 rounded-t-lg shadow-lg">
        {renderSkillButtons(props.data.entities.player_creature.collections.skills)}
        {renderActionButtons()}
      </div>
    </div>
  );
}
