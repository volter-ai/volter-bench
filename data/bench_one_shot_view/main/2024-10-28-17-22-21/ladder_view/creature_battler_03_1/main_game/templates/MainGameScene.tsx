import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Sword, Shield, Zap } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
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
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
}

interface Player {
  uid: string;
  display_name: string;
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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="flex flex-col h-screen w-full max-w-[177.78vh] mx-auto" style={{ aspectRatio: '16/9' }}>
      {/* HUD */}
      <Card uid="hud" className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <div>{props.data.entities.player.display_name}</div>
        <div>{props.data.entities.opponent.display_name}</div>
      </Card>

      {/* Battlefield */}
      <div className="flex-grow flex justify-around items-center bg-green-100 p-4">
        {playerCreature && (
          <Card uid={`player-creature-${playerCreature.uid}`} className="p-4 flex flex-col items-center">
            <h2 className="text-lg font-bold">{playerCreature.display_name}</h2>
            <div className="w-32 h-32 bg-gray-300 rounded-full mb-2"></div>
            <Progress uid={`player-hp-${playerCreature.uid}`} value={(playerCreature.stats.hp / playerCreature.stats.max_hp) * 100} className="w-full" />
            <div className="text-sm">{`HP: ${playerCreature.stats.hp}/${playerCreature.stats.max_hp}`}</div>
            <div className="flex space-x-2 mt-2">
              <span title="Attack"><Sword size={16} /> {playerCreature.stats.attack}</span>
              <span title="Defense"><Shield size={16} /> {playerCreature.stats.defense}</span>
              <span title="Speed"><Zap size={16} /> {playerCreature.stats.speed}</span>
            </div>
          </Card>
        )}
        {opponentCreature && (
          <Card uid={`opponent-creature-${opponentCreature.uid}`} className="p-4 flex flex-col items-center">
            <h2 className="text-lg font-bold">{opponentCreature.display_name}</h2>
            <div className="w-32 h-32 bg-gray-300 rounded-full mb-2"></div>
            <Progress uid={`opponent-hp-${opponentCreature.uid}`} value={(opponentCreature.stats.hp / opponentCreature.stats.max_hp) * 100} className="w-full" />
            <div className="text-sm">{`HP: ${opponentCreature.stats.hp}/${opponentCreature.stats.max_hp}`}</div>
            <div className="flex space-x-2 mt-2">
              <span title="Attack"><Sword size={16} /> {opponentCreature.stats.attack}</span>
              <span title="Defense"><Shield size={16} /> {opponentCreature.stats.defense}</span>
              <span title="Speed"><Zap size={16} /> {opponentCreature.stats.speed}</span>
            </div>
          </Card>
        )}
      </div>

      {/* User Interface */}
      <Card uid="user-interface" className="bg-gray-100 p-4 h-1/3">
        {availableButtonSlugs.length > 0 ? (
          <div className="grid grid-cols-2 gap-4">
            {availableButtonSlugs.map((skillId) => {
              const skill = playerCreature?.collections.skills.find(s => s.meta.prototype_id === skillId);
              return skill ? (
                <Button
                  uid={`skill-${skill.uid}`}
                  key={skill.uid}
                  onClick={() => emitButtonClick(skillId)}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                >
                  {skill.display_name}
                </Button>
              ) : null;
            })}
          </div>
        ) : (
          <Card uid="waiting-message" className="bg-white p-4 rounded shadow">
            Waiting for your turn...
          </Card>
        )}
      </Card>
    </div>
  );
}
