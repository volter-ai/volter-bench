import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap, Heart } from 'lucide-react';
import { Card, CardHeader, CardContent } from "@/components/ui/card";
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

interface GameUIData {
  entities: {
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

function CreatureCard({ creature, isPlayer }: { creature: Creature; isPlayer: boolean }) {
  return (
    <Card className="w-2/5 hover:shadow-lg transition-shadow" key={creature.uid}>
      <CardHeader className="pb-2">
        <h3 className="text-lg font-bold">{creature.display_name}</h3>
      </CardHeader>
      <CardContent>
        <div className="mb-2 bg-gray-200 rounded-full">
          <div 
            className={`${isPlayer ? 'bg-green-500' : 'bg-red-500'} rounded-full h-3`}
            style={{
              width: `${(creature.stats.hp / creature.stats.max_hp) * 100}%`
            }}
          />
        </div>
        <div className="flex gap-3 text-sm">
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

function SkillButton({ skill, onClick }: { skill: Skill; onClick: () => void }) {
  return (
    <Button 
      key={skill.uid}
      onClick={onClick}
      className="w-full h-[100px] flex flex-col items-start p-4 cursor-pointer hover:scale-[1.02] transition-transform"
      variant="default"
      aria-label={`Use skill ${skill.display_name}`}
    >
      <span className="font-bold text-lg">{skill.display_name}</span>
      <span className="text-sm">{skill.description}</span>
      <span className="text-sm mt-1">Damage: {skill.stats.base_damage}</span>
    </Button>
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
    return <div className="w-full min-h-screen flex items-center justify-center">
      Loading battle...
    </div>;
  }

  const availableSkills = playerCreature.collections.skills.filter(skill => 
    availableButtonSlugs.includes(skill.uid)
  );

  return (
    <div className="w-full min-h-screen flex flex-col bg-slate-100">
      <Card className="w-full flex-none h-16 bg-slate-800 text-white rounded-none z-10">
        <CardContent className="flex items-center justify-between p-4">
          <span className="font-bold text-lg">{playerCreature.display_name}</span>
          <span className="font-bold text-lg">{opponentCreature.display_name}</span>
        </CardContent>
      </Card>

      <div className="w-full flex-1 min-h-[400px] flex items-center justify-between px-16 bg-gradient-to-b from-slate-200 to-slate-300">
        <CreatureCard creature={playerCreature} isPlayer={true} />
        <CreatureCard creature={opponentCreature} isPlayer={false} />
      </div>

      <Card className="w-full flex-none min-h-[300px] shadow-inner rounded-none z-20">
        <CardContent className="p-6">
          {availableSkills.length > 0 ? (
            <div className="grid grid-cols-2 gap-6">
              {availableSkills.map((skill) => (
                <SkillButton 
                  key={skill.uid}
                  skill={skill}
                  onClick={() => emitButtonClick(skill.uid)}
                />
              ))}
            </div>
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-500 text-lg">
              Waiting for available actions...
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
