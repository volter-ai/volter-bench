import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap, Heart } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

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

interface GameUIData {
  entities: {
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
    return <div className="aspect-video w-full flex items-center justify-center">
      Loading battle...
    </div>;
  }

  const renderHealthBar = (current: number, max: number) => (
    <div className="w-full bg-gray-200 rounded-full h-2">
      <div
        className="bg-green-600 rounded-full h-2 transition-all duration-300"
        style={{ width: `${(current / max) * 100}%` }}
      />
    </div>
  );

  const renderCreatureStats = (creature: Creature, isPlayer: boolean) => (
    <Card className="p-4 mx-4">
      <div className={`flex flex-col ${isPlayer ? 'items-start' : 'items-end'}`}>
        <h2 className="text-xl font-bold">{creature.display_name}</h2>
        <div className="w-full max-w-[200px]">
          {renderHealthBar(creature.stats.hp, creature.stats.max_hp)}
        </div>
        <div className="flex gap-2 mt-2">
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
    <div className="aspect-video w-full flex flex-col bg-gradient-to-b from-blue-900 to-blue-800">
      {/* HUD */}
      <Card className="w-full p-2 rounded-none bg-black/30">
        <div className="flex justify-between items-center px-4">
          <span className="text-white">Battle Scene</span>
          <Heart className="text-red-500" />
        </div>
      </Card>

      {/* Battlefield */}
      <div className="flex-1 flex items-center justify-center gap-8 px-4">
        <div className="w-1/3 flex justify-center">
          {renderCreatureStats(playerCreature, true)}
        </div>
        <div className="w-1/3 flex justify-center">
          {renderCreatureStats(opponentCreature, false)}
        </div>
      </div>

      {/* Skills UI */}
      <Card className="min-h-[200px] bg-black/40 p-4 rounded-t-xl rounded-b-none">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature.collections.skills.map((skill) => {
            const buttonId = skill.meta.prototype_id;
            return availableButtonSlugs.includes(buttonId) && (
              <Button
                key={skill.uid}
                onClick={() => emitButtonClick(buttonId)}
                variant="secondary"
                className="h-auto flex flex-col items-start p-4"
              >
                <h3 className="font-bold">{skill.display_name}</h3>
                <p className="text-sm opacity-80">{skill.description}</p>
                <span className="text-xs mt-1">Damage: {skill.stats.base_damage}</span>
              </Button>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
