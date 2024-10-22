import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Heart, Zap } from 'lucide-react';

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
  meta: {
    skill_type: string;
    is_physical: boolean;
  };
}

interface Creature {
  uid: string;
  display_name: string;
  description: string;
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
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
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

const CreatureDisplay = ({ creature, isPlayer, uid }: { creature: Creature; isPlayer: boolean; uid: string }) => (
  <div className={`flex flex-col items-center ${isPlayer ? 'justify-end' : 'justify-start'}`} key={uid}>
    <div className="w-32 h-32 bg-gray-300 rounded-full mb-2"></div>
    <div className="text-center">
      <h3 className="font-bold">{creature.display_name}</h3>
      <div className="flex items-center">
        <Heart className="w-4 h-4 mr-1" />
        <div className="w-24 bg-gray-200 rounded-full h-2.5">
          <div
            className="bg-green-600 h-2.5 rounded-full"
            style={{ width: `${(creature.stats.hp / creature.stats.max_hp) * 100}%` }}
          ></div>
        </div>
      </div>
    </div>
  </div>
);

const BattlefieldDisplay = ({ playerCreature, opponentCreature, uid }: { playerCreature: Creature; opponentCreature: Creature; uid: string }) => (
  <div className="h-2/3 flex flex-col justify-between p-4" key={uid}>
    <div className="flex justify-between">
      <CreatureDisplay creature={opponentCreature} isPlayer={false} uid={opponentCreature.uid} />
      <div className="text-right">
        <h3 className="font-bold">{opponentCreature.display_name}</h3>
        <p>HP: {opponentCreature.stats.hp}/{opponentCreature.stats.max_hp}</p>
      </div>
    </div>
    <div className="flex justify-between">
      <div>
        <h3 className="font-bold">{playerCreature.display_name}</h3>
        <p>HP: {playerCreature.stats.hp}/{playerCreature.stats.max_hp}</p>
      </div>
      <CreatureDisplay creature={playerCreature} isPlayer={true} uid={playerCreature.uid} />
    </div>
  </div>
);

const UserInterface = ({ availableButtonSlugs, emitButtonClick, enabledUIDs, uid }: { availableButtonSlugs: string[]; emitButtonClick: (slug: string) => void; enabledUIDs: string[]; uid: string }) => (
  <div className="h-1/3 bg-gray-100 p-4" key={uid}>
    <div className="grid grid-cols-2 gap-4">
      {availableButtonSlugs.map((slug) => (
        <button
          key={slug}
          onClick={() => emitButtonClick(slug)}
          className={`font-bold py-2 px-4 rounded ${enabledUIDs.includes(slug) ? 'bg-blue-500 hover:bg-blue-700 text-white' : 'bg-gray-300 text-gray-500 cursor-not-allowed'}`}
          disabled={!enabledUIDs.includes(slug)}
        >
          {slug.charAt(0).toUpperCase() + slug.slice(1)}
        </button>
      ))}
    </div>
  </div>
);

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full bg-gray-200 flex flex-col" style={{ aspectRatio: '16/9' }}>
      <BattlefieldDisplay 
        playerCreature={playerCreature} 
        opponentCreature={opponentCreature} 
        uid="battlefield"
      />
      <UserInterface 
        availableButtonSlugs={availableButtonSlugs} 
        emitButtonClick={emitButtonClick} 
        enabledUIDs={enabledUIDs}
        uid="user-interface"
      />
    </div>
  );
}
