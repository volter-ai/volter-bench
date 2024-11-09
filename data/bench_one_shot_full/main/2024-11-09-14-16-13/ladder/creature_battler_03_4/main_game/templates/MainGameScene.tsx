import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap, Heart } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

interface ExamplePlayer {
    uid: string;
    stats: {
        stat1: number;
    };
}

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
        player: ExamplePlayer;
        opponent: ExamplePlayer;
        player_creature: Creature;
        opponent_creature: Creature;
    };
}

function CreatureCard({ creature, isPlayer }: { creature: Creature; isPlayer: boolean }) {
    return (
        <Card className="w-[300px] p-4 bg-slate-800 border-slate-700">
            <div className="flex justify-between items-center mb-2">
                <h3 className="text-lg font-bold text-white">{creature.display_name}</h3>
                <span className="text-sm text-slate-400">{isPlayer ? 'Player' : 'Opponent'}</span>
            </div>
            
            <div className="space-y-2">
                <div>
                    <div className="flex justify-between text-sm text-slate-300 mb-1">
                        <span>HP</span>
                        <span>{creature.stats.hp}/{creature.stats.max_hp}</span>
                    </div>
                    <Progress 
                        value={(creature.stats.hp / creature.stats.max_hp) * 100}
                        className="h-2"
                    />
                </div>
                
                <div className="flex gap-4 text-sm text-slate-300">
                    <div className="flex items-center gap-1">
                        <Sword className="w-4 h-4" />
                        {creature.stats.attack}
                    </div>
                    <div className="flex items-center gap-1">
                        <Shield className="w-4 h-4" />
                        {creature.stats.defense}
                    </div>
                    <div className="flex items-center gap-1">
                        <Zap className="w-4 h-4" />
                        {creature.stats.speed}
                    </div>
                </div>
            </div>
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
            <div className="w-full h-full flex items-center justify-center text-white">
                Loading battle...
            </div>
        );
    }

    return (
        <div className="w-full h-full flex flex-col bg-slate-900">
            {/* HUD */}
            <Card className="h-[10%] rounded-none border-b border-slate-700 flex items-center px-6">
                <div className="flex items-center gap-2 text-white">
                    <Heart className="text-red-500" />
                    Battle Scene
                </div>
            </Card>

            {/* Battlefield */}
            <div className="h-[50%] flex justify-between items-center px-12">
                <CreatureCard creature={playerCreature} isPlayer={true} />
                <CreatureCard creature={opponentCreature} isPlayer={false} />
            </div>

            {/* UI Region */}
            <Card className="h-[40%] mt-auto rounded-t-xl border-slate-700">
                {/* Text Display Area */}
                <div className="h-1/3 p-4 border-b border-slate-700">
                    <p className="text-slate-300">
                        What will {playerCreature.display_name} do?
                    </p>
                </div>

                {/* Skills Area */}
                <div className="h-2/3 p-4">
                    <div className="grid grid-cols-2 gap-4">
                        {playerCreature.collections.skills?.map((skill) => (
                            <Button
                                key={skill.uid}
                                variant="secondary"
                                onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
                                disabled={!availableButtonSlugs.includes(skill.display_name.toLowerCase())}
                                className="h-auto p-4 flex flex-col items-start"
                            >
                                <span className="font-bold">{skill.display_name}</span>
                                <span className="text-sm text-slate-400">{skill.description}</span>
                                <span className="text-sm mt-1">Damage: {skill.stats.base_damage}</span>
                            </Button>
                        ))}
                    </div>
                </div>
            </Card>
        </div>
    );
}
