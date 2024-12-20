import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap, Heart } from 'lucide-react';
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
    return <div className="w-full h-screen flex items-center justify-center">
      Loading battle...
    </div>;
  }

  const renderCreatureStats = (creature: Creature, isPlayer: boolean) => (
    <Card className={`p-4 ${isPlayer ? 'mr-auto' : 'ml-auto'} w-64`}>
      <div className="flex flex-col gap-2">
        <h2 className="text-xl font-bold">{creature.display_name}</h2>
        <div className="w-full">
          <Progress 
            value={(creature.stats.hp / creature.stats.max_hp) * 100}
            className="h-2"
          />
          <span className="text-sm">
            {creature.stats.hp}/{creature.stats.max_hp} HP
          </span>
        </div>
        <div className="flex gap-4 mt-2">
          <div className="flex items-center">
            <Sword className="w-4 h-4 mr-1" />
            {creature.stats.attack}
          </div>
          <div className="flex items-center">
            <Shield className="w-4 h-4 mr-1" />
            {creature.stats.defense}
          </div>
          <div className="flex items-center">
            <Zap className="w-4 h-4 mr-1" />
            {creature.stats.speed}
          </div>
        </div>
      </div>
    </Card>
  );

  return (
    <div className="w-full h-screen flex flex-col bg-gradient-to-b from-blue-900 to-blue-800">
      <Card className="w-full p-4 rounded-none bg-black/30">
        <div className="flex justify-between items-center">
          <span className="text-white">Battle Scene</span>
          <Heart className="text-red-500" />
        </div>
      </Card>

      <div className="flex-1 p-8">
        <div className="flex justify-between items-center h-full">
          <div className="w-1/3 flex flex-col items-start">
            <div className="text-white text-center w-full mb-4">Player</div>
            {renderCreatureStats(playerCreature, true)}
          </div>
          <div className="w-1/3 flex flex-col items-end">
            <div className="text-white text-center w-full mb-4">Opponent</div>
            {renderCreatureStats(opponentCreature, false)}
          </div>
        </div>
      </div>

      <Card className="min-h-[200px] max-h-[40%] bg-black/40 p-4 rounded-t-xl rounded-b-none">
        <div className="grid grid-cols-2 gap-4 h-full overflow-y-auto">
          {playerCreature.collections.skills.map((skill) => {
            const buttonId = skill.meta.prototype_id;
            const isAvailable = availableButtonSlugs.includes(buttonId);
            
            return (
              <Button
                key={skill.uid}
                onClick={() => isAvailable && emitButtonClick(buttonId)}
                variant="secondary"
                className="h-auto flex flex-col items-start p-4"
                disabled={!isAvailable}
              >
                <h3 className="font-bold">{skill.display_name}</h3>
                <p className="text-sm opacity-80">{skill.description}</p>
                <span className="text-xs">Damage: {skill.stats.base_damage}</span>
              </Button>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
