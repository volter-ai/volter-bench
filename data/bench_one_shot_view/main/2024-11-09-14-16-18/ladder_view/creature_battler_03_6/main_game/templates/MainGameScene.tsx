import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

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
  meta: {
    prototype_id: string;
  };
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
  meta: {
    prototype_id: string;
  };
}

interface GameUIData {
  entities: {
    player: {
      uid: string;
      stats: Record<string, number>;
    };
    opponent: {
      uid: string;
      stats: Record<string, number>;
    };
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data?.entities?.player_creature;
  const opponentCreature = props.data?.entities?.opponent_creature;

  if (!playerCreature || !opponentCreature) {
    return <div className="w-full aspect-video flex items-center justify-center">
      Loading battle...
    </div>;
  }

  return (
    <div className="w-full aspect-video flex flex-col bg-slate-100">
      {/* HUD */}
      <Card className="w-full h-[10%] bg-slate-800 text-white px-4 flex items-center justify-between rounded-none">
        <div className="flex items-center gap-2">
          <span className="font-bold">{playerCreature.display_name}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="font-bold">{opponentCreature.display_name}</span>
        </div>
      </Card>

      {/* Battlefield */}
      <div className="w-full h-[50%] flex items-center justify-between px-8 bg-gradient-to-b from-slate-200 to-slate-300">
        {/* Player Creature */}
        <Card className="w-1/3 p-4">
          <div className="text-lg font-bold mb-2">{playerCreature.display_name}</div>
          <div className="mb-2">
            <Progress 
              value={(playerCreature.stats.hp / playerCreature.stats.max_hp) * 100}
              className="h-2"
            />
            <div className="text-sm text-center">
              HP: {playerCreature.stats.hp}/{playerCreature.stats.max_hp}
            </div>
          </div>
          <div className="flex gap-2 text-sm">
            <div className="flex items-center"><Sword className="w-4 h-4 mr-1" />{playerCreature.stats.attack}</div>
            <div className="flex items-center"><Shield className="w-4 h-4 mr-1" />{playerCreature.stats.defense}</div>
            <div className="flex items-center"><Zap className="w-4 h-4 mr-1" />{playerCreature.stats.speed}</div>
          </div>
        </Card>

        {/* Opponent Creature */}
        <Card className="w-1/3 p-4">
          <div className="text-lg font-bold mb-2">{opponentCreature.display_name}</div>
          <div className="mb-2">
            <Progress 
              value={(opponentCreature.stats.hp / opponentCreature.stats.max_hp) * 100}
              className="h-2"
            />
            <div className="text-sm text-center">
              HP: {opponentCreature.stats.hp}/{opponentCreature.stats.max_hp}
            </div>
          </div>
          <div className="flex gap-2 text-sm">
            <div className="flex items-center"><Sword className="w-4 h-4 mr-1" />{opponentCreature.stats.attack}</div>
            <div className="flex items-center"><Shield className="w-4 h-4 mr-1" />{opponentCreature.stats.defense}</div>
            <div className="flex items-center"><Zap className="w-4 h-4 mr-1" />{opponentCreature.stats.speed}</div>
          </div>
        </Card>
      </div>

      {/* Skills UI */}
      <Card className="w-full h-[40%] p-4 rounded-none">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature.collections.skills.map((skill) => (
            availableButtonSlugs.includes(skill.meta.prototype_id) && (
              <Button
                key={skill.uid}
                onClick={() => emitButtonClick(skill.meta.prototype_id)}
                variant="default"
                className="h-auto flex flex-col items-start p-4"
              >
                <div className="font-bold">{skill.display_name}</div>
                <div className="text-sm">{skill.description}</div>
                <div className="text-sm mt-1">Damage: {skill.stats.base_damage}</div>
              </Button>
            )
          ))}
        </div>
      </Card>
    </div>
  );
}
