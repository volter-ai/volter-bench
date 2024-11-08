import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap, Heart } from 'lucide-react';
import { Card, CardHeader, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress"; 

interface Skill {
  uid: string;
  meta: {
    prototype_id: string;
    skill_type: string;
  };
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
  meta: {
    creature_type: string;
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

function CreatureCard({ creature, isPlayer }: { creature: Creature; isPlayer: boolean }) {
  const healthPercent = (creature.stats.hp / creature.stats.max_hp) * 100;
  
  return (
    <Card className="w-1/3" key={creature.uid}>
      <CardHeader>
        <div className="flex justify-between items-center">
          <h3 className="font-bold text-lg">{creature.display_name}</h3>
          <span className="text-sm text-muted-foreground">
            {isPlayer ? "Player" : "Opponent"}
          </span>
        </div>
      </CardHeader>
      <CardContent>
        <Progress 
          value={healthPercent}
          className={`${isPlayer ? "bg-green-200" : "bg-red-200"}`}
        />
        <div className="flex gap-2 mt-2 text-sm">
          <div className="flex items-center">
            <Heart className="w-4 h-4 mr-1" />
            {creature.stats.hp}/{creature.stats.max_hp}
          </div>
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
      </CardContent>
    </Card>
  );
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data?.entities?.player_creature;
  const opponentCreature = props.data?.entities?.opponent_creature;

  if (!playerCreature || !opponentCreature) {
    return (
      <div className="w-full h-screen flex items-center justify-center">
        <Card>
          <CardContent>Loading battle...</CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="w-full h-screen flex flex-col bg-background">
      {/* HUD */}
      <nav className="w-full h-[10%] bg-primary text-primary-foreground px-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="font-bold">{playerCreature.display_name}</span>
          <span className="text-sm">Type: {playerCreature.meta.creature_type}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="font-bold">{opponentCreature.display_name}</span>
          <span className="text-sm">Type: {opponentCreature.meta.creature_type}</span>
        </div>
      </nav>

      {/* Battlefield */}
      <div className="w-full h-[50%] flex items-center justify-between px-8 bg-gradient-to-b from-background to-muted">
        <CreatureCard creature={playerCreature} isPlayer={true} />
        <CreatureCard creature={opponentCreature} isPlayer={false} />
      </div>

      {/* Action UI */}
      <Card className="w-full h-[40%] shadow-inner">
        <CardContent className="p-4">
          <div className="grid grid-cols-2 gap-4">
            {playerCreature.collections.skills.map((skill) => (
              availableButtonSlugs.includes(skill.meta.prototype_id) && (
                <Button
                  key={skill.uid}
                  onClick={() => emitButtonClick(skill.meta.prototype_id)}
                  variant="default"
                  className="h-auto flex flex-col items-start p-4"
                >
                  <span className="font-bold">{skill.display_name}</span>
                  <span className="text-sm">{skill.description}</span>
                  <span className="text-sm mt-1">
                    Damage: {skill.stats.base_damage} | Type: {skill.meta.skill_type}
                  </span>
                </Button>
              )
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
