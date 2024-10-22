import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { Sword, ArrowLeft, X, Home } from 'lucide-react';

interface Skill {
  __type: "Skill";
  stats: {
    base_damage: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    skill_type: string;
    is_physical: boolean;
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
    sp_attack: number;
    sp_defense: number;
    speed: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
  uid: string;
  display_name: string;
  description: string;
}

interface Player {
  __type: "Player";
  entities: {
    active_creature: Creature;
  };
  collections: {
    creatures: Creature[];
  };
  uid: string;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
  };
  meta: {
    battle_ended: boolean;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player.entities.active_creature;
  const opponentCreature = props.data.entities.opponent.entities.active_creature;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="col-start-1 row-start-1 flex flex-col items-start justify-start">
          <h3 className="text-lg font-bold">{opponentCreature?.display_name}</h3>
          <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
            <div 
              className="bg-blue-600 h-2.5 rounded-full" 
              style={{ width: `${((opponentCreature?.stats.hp ?? 0) / (opponentCreature?.stats.max_hp ?? 1)) * 100}%` }}
            ></div>
          </div>
          <p className="text-sm">HP: {opponentCreature?.stats.hp}/{opponentCreature?.stats.max_hp}</p>
        </div>

        {/* Opponent Creature */}
        <div className="col-start-2 row-start-1 flex justify-end items-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image={`/images/creatures/${opponentCreature.meta.prototype_id}_front.png`}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Player Creature */}
        <div className="col-start-1 row-start-2 flex items-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image={`/images/creatures/${playerCreature.meta.prototype_id}_back.png`}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Player Creature Status */}
        <div className="col-start-2 row-start-2 flex flex-col items-end justify-end">
          <h3 className="text-lg font-bold">{playerCreature?.display_name}</h3>
          <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
            <div 
              className="bg-green-600 h-2.5 rounded-full" 
              style={{ width: `${((playerCreature?.stats.hp ?? 0) / (playerCreature?.stats.max_hp ?? 1)) * 100}%` }}
            ></div>
          </div>
          <p className="text-sm">HP: {playerCreature?.stats.hp}/{playerCreature?.stats.max_hp}</p>
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {availableButtonSlugs.includes('attack') && (
            <SkillButton
              uid="attack"
              skillName="Attack"
              description="Perform a basic attack"
              stats="Damage varies"
              onClick={() => emitButtonClick('attack')}
            >
              <Sword className="mr-2" /> Attack
            </SkillButton>
          )}
          {availableButtonSlugs.includes('swap') && (
            <SkillButton
              uid="swap"
              skillName="Swap"
              description="Switch to another creature"
              stats="No cost"
              onClick={() => emitButtonClick('swap')}
            >
              <ArrowLeft className="mr-2" /> Swap
            </SkillButton>
          )}
          {availableButtonSlugs.includes('back') && (
            <SkillButton
              uid="back"
              skillName="Back"
              description="Go back to the previous screen"
              stats="No cost"
              onClick={() => emitButtonClick('back')}
            >
              <ArrowLeft className="mr-2" /> Back
            </SkillButton>
          )}
          {availableButtonSlugs.includes('quit-game') && (
            <SkillButton
              uid="quit-game"
              skillName="Quit Game"
              description="Exit the current game"
              stats="No cost"
              onClick={() => emitButtonClick('quit-game')}
            >
              <X className="mr-2" /> Quit Game
            </SkillButton>
          )}
          {availableButtonSlugs.includes('return-to-main-menu') && (
            <SkillButton
              uid="return-to-main-menu"
              skillName="Main Menu"
              description="Return to the main menu"
              stats="No cost"
              onClick={() => emitButtonClick('return-to-main-menu')}
            >
              <Home className="mr-2" /> Main Menu
            </SkillButton>
          )}
        </div>
      </div>

      {/* Player Cards (hidden, but included for potential future use) */}
      <div className="hidden">
        {props.data.entities.player && (
          <PlayerCard
            uid={props.data.entities.player.uid}
            playerName={props.data.entities.player.display_name}
            imageUrl={`/images/players/${props.data.entities.player.uid}.png`}
          />
        )}
        {props.data.entities.opponent && (
          <PlayerCard
            uid={props.data.entities.opponent.uid}
            playerName={props.data.entities.opponent.display_name}
            imageUrl={`/images/players/${props.data.entities.opponent.uid}.png`}
          />
        )}
      </div>
    </div>
  );
}
