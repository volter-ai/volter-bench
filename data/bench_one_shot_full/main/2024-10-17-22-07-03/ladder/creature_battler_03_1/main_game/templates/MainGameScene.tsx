import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

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
}

interface Player {
  uid: string;
  display_name: string;
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
  const { enabledUIDs } = useThingInteraction();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <PlayerCard
          uid={props.data.entities.player.uid}
          playerName={props.data.entities.player.display_name}
          imageUrl={`/images/players/${props.data.entities.player.uid}.jpg`}
        />
        <PlayerCard
          uid={props.data.entities.opponent.uid}
          playerName={props.data.entities.opponent.display_name}
          imageUrl={`/images/players/${props.data.entities.opponent.uid}.jpg`}
        />
      </div>

      {/* Battlefield */}
      <div className="flex-grow grid grid-cols-2 gap-4 p-4">
        <div className="flex justify-center items-center">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl={`/images/creatures/${playerCreature.uid}.jpg`}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
        <div className="flex justify-center items-center">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl={`/images/creatures/${opponentCreature.uid}.jpg`}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t border-gray-300">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <h3 className="font-bold text-lg">Skills</h3>
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
          <div className="space-y-2">
            <h3 className="font-bold text-lg">Actions</h3>
            {['play-again', 'quit'].map((action) => (
              <Button
                key={action}
                disabled={!availableButtonSlugs.includes(action)}
                onClick={() => emitButtonClick(action)}
                className="w-full"
              >
                {action === 'play-again' ? 'Play Again' : 'Quit'}
              </Button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
