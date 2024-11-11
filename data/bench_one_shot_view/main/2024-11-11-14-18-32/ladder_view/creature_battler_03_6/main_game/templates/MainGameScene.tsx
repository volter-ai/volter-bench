import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface Creature {
    __type: "Creature";
    stats: {
        hp: number;
        max_hp: number;
        attack: number;
        defense: number;
        speed: number;
    };
    meta: {
        prototype_id: string;
        category: string;
        creature_type: string;
    };
    collections: {
        skills: Skill[];
    };
    uid: string;
    display_name: string;
    description: string;
}

interface Skill {
    __type: "Skill";
    stats: {
        base_damage: number;
    };
    meta: {
        prototype_id: string;
        category: string;
        skill_type: string;
    };
    uid: string;
    display_name: string;
    description: string;
}

interface Player {
    __type: "Player";
    meta: {
        prototype_id: string;
        category: string;
    };
    collections: {
        creatures: Creature[];
    };
    uid: string;
    display_name: string;
    description: string;
}

interface GameUIData {
    entities: {
        player: Player;
        opponent: Player;
        player_creature: Creature;
        opponent_creature: Creature;
    };
    uid: string;
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

    return (
        <div className="w-full h-screen flex flex-col bg-slate-100">
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
                    <div className="mb-2 bg-gray-200 rounded-full">
                        <div 
                            className="bg-green-500 rounded-full px-2 py-1 text-white text-sm"
                            style={{ width: `${(playerCreature.stats.hp / playerCreature.stats.max_hp) * 100}%` }}
                        >
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
                    <div className="mb-2 bg-gray-200 rounded-full">
                        <div 
                            className="bg-red-500 rounded-full px-2 py-1 text-white text-sm"
                            style={{ width: `${(opponentCreature.stats.hp / opponentCreature.stats.max_hp) * 100}%` }}
                        >
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
