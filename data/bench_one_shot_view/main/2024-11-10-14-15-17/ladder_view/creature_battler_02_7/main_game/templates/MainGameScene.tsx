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

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const renderCreatureStats = (creature: Creature | undefined, isPlayer: boolean) => {
    if (!creature) return null;
    
    return (
      <Card className={`p-4 ${isPlayer ? 'bg-slate-800' : 'bg-slate-700'}`}>
        <h2 className="text-xl font-bold">{creature.display_name}</h2>
        <div className="flex flex-col gap-2 mt-2">
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
    <div className="w-full h-full flex flex-col bg-slate-900 text-white" style={{ aspectRatio: '16/9' }}>
      {/* HUD */}
      <Card className="h-[10%] bg-slate-800 px-4 flex items-center justify-between rounded-none">
        <span>{props.data.entities.player?.display_name}</span>
        <span>{props.data.entities.opponent?.display_name}</span>
      </Card>

      {/* Battlefield */}
      <div className="h-[50%] flex items-center justify-between px-8 bg-slate-900">
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
      <Card className="h-[40%] flex flex-col gap-4 p-4">
        {/* Text Display Area */}
        <Card className="flex-1 p-4 bg-slate-800 overflow-y-auto">
          <p className="text-slate-200">
            {/* Game text would be injected here from props/state */}
            What will {props.data.entities.player_creature?.display_name} do?
          </p>
        </Card>

        {/* Skills Buttons Area */}
        <div className="grid grid-cols-2 gap-4">
          {props.data.entities.player_creature?.collections.skills.map((skill) => (
            availableButtonSlugs.includes(skill.display_name.toLowerCase()) && (
              <Button
                key={skill.uid}
                variant="secondary"
                onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
                className="w-full h-full flex flex-col items-start p-4"
              >
                <span className="font-bold">{skill.display_name}</span>
                <span className="text-sm text-slate-300">{skill.description}</span>
              </Button>
            )
          ))}
        </div>
      </Card>
    </div>
  );
}
