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

  if (!props.data?.entities) {
    return <div className="w-full h-full flex items-center justify-center">Loading...</div>;
  }

  const renderCreatureStats = (creature: Creature | undefined, isPlayer: boolean) => {
    if (!creature) return null;
    
    return (
      <Card className={`p-4 ${isPlayer ? 'ml-8' : 'mr-8'}`}>
        <div className={`flex flex-col ${isPlayer ? 'items-start' : 'items-end'} gap-2`}>
          <h2 className="text-xl font-bold">{creature.display_name}</h2>
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
      <Card className="w-full p-4 rounded-none bg-slate-800 flex items-center justify-between">
        <span>{props.data.entities.player?.display_name}</span>
        <span>{props.data.entities.opponent?.display_name}</span>
      </Card>

      {/* Battlefield */}
      <div className="flex-1 flex items-center justify-between">
        <div className="flex flex-col items-center">
          <div className="text-sm text-blue-400 mb-2">Player</div>
          {renderCreatureStats(props.data.entities.player_creature, true)}
        </div>
        
        <div className="flex flex-col items-center">
          <div className="text-sm text-red-400 mb-2">Opponent</div>
          {renderCreatureStats(props.data.entities.opponent_creature, false)}
        </div>
      </div>

      {/* UI Area */}
      <Card className="p-4 rounded-none bg-slate-800">
        <div className="grid grid-cols-2 gap-4">
          {props.data.entities.player_creature?.collections.skills.map((skill) => {
            const skillId = skill.meta?.prototype_id || skill.display_name.toLowerCase();
            return availableButtonSlugs.includes(skillId) && (
              <Button
                key={skill.uid}
                variant="secondary"
                onClick={() => emitButtonClick(skillId)}
                className="w-full h-full flex flex-col items-start p-4"
              >
                <span className="font-bold">{skill.display_name}</span>
                <span className="text-sm text-muted-foreground">{skill.description}</span>
              </Button>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
