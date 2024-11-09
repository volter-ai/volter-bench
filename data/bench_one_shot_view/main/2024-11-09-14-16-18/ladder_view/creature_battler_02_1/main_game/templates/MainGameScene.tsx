import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Heart } from 'lucide-react';
import { Card } from "@/components/ui/card";
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
  description: string;
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

const CreatureDisplay = ({ creature, isPlayer }: { creature: Creature, isPlayer: boolean }) => {
  if (!creature) return null;
  
  return (
    <Card className="flex flex-col items-center p-4">
      <div className="text-white mb-2">{creature.display_name}</div>
      <div className="w-48 h-48 bg-slate-700 rounded-lg flex items-center justify-center" 
           aria-label={`${isPlayer ? 'Player' : 'Opponent'} creature display area`}>
        <span className="text-white">
          {isPlayer ? "Player's" : "Opponent's"} {creature.display_name}
        </span>
      </div>
      <div className="mt-2 flex gap-2" aria-label="Health status">
        <Heart className="text-red-500" />
        <span className="text-white">
          {creature.stats.hp}/{creature.stats.max_hp}
        </span>
      </div>
      <div className="flex gap-2 mt-1">
        <div className="flex items-center" aria-label="Attack stat">
          <Sword className="text-gray-400 w-4 h-4" />
          <span className="text-white text-sm">{creature.stats.attack}</span>
        </div>
        <div className="flex items-center" aria-label="Defense stat">
          <Shield className="text-gray-400 w-4 h-4" />
          <span className="text-white text-sm">{creature.stats.defense}</span>
        </div>
      </div>
    </Card>
  );
};

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data?.entities?.player_creature;
  const opponentCreature = props.data?.entities?.opponent_creature;

  if (!playerCreature || !opponentCreature) {
    return (
      <div className="w-full aspect-video flex items-center justify-center">
        <Card className="p-4">Loading battle...</Card>
      </div>
    );
  }

  return (
    <div className="w-full aspect-video flex flex-col bg-slate-900">
      {/* HUD */}
      <Card className="h-16 bg-slate-800 flex items-center justify-between px-4">
        <div className="text-white font-bold">
          {props.data.entities.player?.display_name || 'Player'}
        </div>
        <div className="text-white font-bold">
          Battle Scene
        </div>
      </Card>

      {/* Battlefield */}
      <div className="flex-1 flex items-center justify-between px-8" 
           role="region" 
           aria-label="Battle field">
        <CreatureDisplay creature={playerCreature} isPlayer={true} />
        <CreatureDisplay creature={opponentCreature} isPlayer={false} />
      </div>

      {/* Action UI */}
      <Card className="h-1/3 bg-slate-800 p-4">
        <div className="grid grid-cols-2 gap-2">
          {playerCreature.collections.skills?.map((skill) => (
            <Button
              key={skill.uid}
              variant={availableButtonSlugs.includes(skill.display_name.toLowerCase()) 
                ? "default" 
                : "secondary"}
              onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
              disabled={!availableButtonSlugs.includes(skill.display_name.toLowerCase())}
              className="h-auto flex flex-col items-start p-4"
              aria-label={`Use ${skill.display_name} skill`}
            >
              <span className="font-bold">{skill.display_name}</span>
              <span className="text-sm opacity-90">{skill.description}</span>
            </Button>
          ))}
        </div>
      </Card>
    </div>
  );
}
