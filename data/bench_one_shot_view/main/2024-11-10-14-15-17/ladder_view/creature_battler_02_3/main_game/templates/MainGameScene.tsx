import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Heart } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  meta: {
    prototype_id: string;
  };
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

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  if (!props.data?.entities) {
    return <div className="w-full h-full flex items-center justify-center">Loading...</div>;
  }

  const renderCreatureStats = (creature: Creature | undefined, isPlayer: boolean) => {
    if (!creature) return null;
    
    return (
      <Card className={`p-4 ${isPlayer ? 'bg-slate-800' : 'bg-slate-700'}`}>
        <h2 className="text-xl font-bold mb-2">{creature.display_name}</h2>
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Heart className="h-4 w-4 text-red-500" />
            <span>{creature.stats.hp}/{creature.stats.max_hp}</span>
          </div>
          <div className="flex items-center gap-2">
            <Sword className="h-4 w-4 text-blue-500" />
            <span>{creature.stats.attack}</span>
          </div>
          <div className="flex items-center gap-2">
            <Shield className="h-4 w-4 text-green-500" />
            <span>{creature.stats.defense}</span>
          </div>
        </div>
      </Card>
    );
  };

  return (
    <div className="w-full h-full flex flex-col bg-slate-900 text-white aspect-video">
      {/* HUD */}
      <Card className="h-[10%] bg-slate-800 px-4 flex items-center justify-between rounded-none">
        <span>{props.data.entities.player?.display_name}</span>
        <span>{props.data.entities.opponent?.display_name}</span>
      </Card>

      {/* Battlefield */}
      <div className="h-[60%] flex items-center justify-between px-8">
        <div className="flex flex-col items-center gap-4">
          <div className="text-sm text-blue-400">Player</div>
          {renderCreatureStats(props.data.entities.player_creature, true)}
        </div>
        
        <div className="flex flex-col items-center gap-4">
          <div className="text-sm text-red-400">Opponent</div>
          {renderCreatureStats(props.data.entities.opponent_creature, false)}
        </div>
      </div>

      {/* UI Area */}
      <Card className="h-[30%] bg-slate-800 p-4 rounded-none rounded-t-xl">
        <div className="grid grid-cols-2 gap-4">
          {props.data.entities.player_creature?.collections.skills.map((skill) => (
            availableButtonSlugs.includes(skill.meta.prototype_id) && (
              <Button
                key={skill.uid}
                variant="secondary"
                onClick={() => emitButtonClick(skill.meta.prototype_id)}
                className="h-auto flex flex-col items-start p-3"
              >
                <div className="font-bold">{skill.display_name}</div>
                <div className="text-sm text-slate-300">{skill.description}</div>
              </Button>
            )
          ))}
        </div>
      </Card>
    </div>
  );
}
