import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Sword, RefreshCw } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  meta: {
    creature_type: string;
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
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const playerCreature = props.data.entities.player.collections.creatures[0];
  const opponentCreature = props.data.entities.opponent.collections.creatures[0];

  return (
    <div className="h-screen w-screen flex flex-col">
      {/* Battlefield Display */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Status */}
        <div className="row-start-1 col-start-1 flex justify-start items-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image={`/images/creatures/${opponentCreature.meta.creature_type}.png`}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Opponent Creature */}
        <div className="row-start-1 col-start-2 flex justify-end items-start">
          <PlayerCard
            uid={props.data.entities.opponent.uid}
            playerName={props.data.entities.opponent.display_name}
            imageUrl="/images/opponent.png"
          />
        </div>

        {/* Player Creature */}
        <div className="row-start-2 col-start-1 flex justify-start items-end">
          <PlayerCard
            uid={props.data.entities.player.uid}
            playerName={props.data.entities.player.display_name}
            imageUrl="/images/player.png"
          />
        </div>

        {/* Player Status */}
        <div className="row-start-2 col-start-2 flex justify-end items-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image={`/images/creatures/${playerCreature.meta.creature_type}.png`}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4">
          {availableButtonSlugs.includes('attack') && (
            <SkillButton
              uid="attack-button"
              skillName="Attack"
              description="Perform a basic attack"
              stats="Damage: 5"
              onClick={() => emitButtonClick('attack')}
            >
              <Sword className="mr-2 h-4 w-4" /> Attack
            </SkillButton>
          )}
          {availableButtonSlugs.includes('swap') && (
            <Button
              onClick={() => emitButtonClick('swap')}
            >
              <RefreshCw className="mr-2 h-4 w-4" /> Swap Creature
            </Button>
          )}
          {/* Add more buttons here as needed */}
        </div>
      </div>
    </div>
  );
}
