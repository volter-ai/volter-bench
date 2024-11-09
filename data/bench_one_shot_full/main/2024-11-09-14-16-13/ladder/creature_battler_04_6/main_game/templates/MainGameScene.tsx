import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Heart } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface Skill {
    uid: string;
    stats: {
        base_damage: number;
    };
    meta: {
        prototype_id: string;
        skill_type: string;
        is_physical: boolean;
    };
    display_name: string;
    description: string;
}

interface Creature {
    uid: string;
    stats: {
        hp: number;
        max_hp: number;
        attack: number;
        defense: number;
        sp_attack: number;
        sp_defense: number;
        speed: number;
    };
    meta: {
        prototype_id: string;
        creature_type: string;
    };
    collections: {
        skills: Skill[];
    };
    display_name: string;
    description: string;
}

interface Player {
    uid: string;
    stats: Record<string, number>;
    meta: {
        prototype_id: string;
        category: string;
    };
    collections: {
        creatures: Creature[];
    };
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

const HealthBar = ({ current, max }: { current: number; max: number }) => (
    <div className="w-full h-2 bg-gray-200 rounded">
        <div
            className="h-full bg-green-500 rounded transition-all duration-300"
            style={{ width: `${Math.max(0, Math.min(100, (current / max) * 100))}%` }}
        />
    </div>
);

const CreatureStats = ({ creature, uid }: { creature: Creature; uid: string }) => (
    <Card className="p-4" key={uid}>
        <div className="flex flex-col gap-2">
            <div className="flex justify-between items-center">
                <span className="font-bold">{creature.display_name}</span>
                <span className="text-sm">
                    {creature.stats.hp}/{creature.stats.max_hp} HP
                </span>
            </div>
            <HealthBar current={creature.stats.hp} max={creature.stats.max_hp} />
            <div className="flex gap-2 text-sm">
                <div className="flex items-center gap-1">
                    <Sword size={16} />
                    {creature.stats.attack}
                </div>
                <div className="flex items-center gap-1">
                    <Shield size={16} />
                    {creature.stats.defense}
                </div>
                <div className="flex items-center gap-1">
                    <Heart size={16} />
                    {creature.stats.speed}
                </div>
            </div>
        </div>
    </Card>
);

export function MainGameSceneView(props: { data: GameUIData }) {
    const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
    const { player_creature, opponent_creature } = props.data.entities;

    return (
        <div className="w-full h-full aspect-[16/9] flex flex-col bg-slate-900">
            {/* Battlefield Area */}
            <div className="flex-grow-2 grid grid-cols-2 grid-rows-2 gap-4 p-4">
                {/* Opponent Stats */}
                <div className="col-start-1 row-start-1">
                    {opponent_creature && (
                        <CreatureStats 
                            creature={opponent_creature} 
                            uid={opponent_creature.uid} 
                        />
                    )}
                </div>
                
                {/* Opponent Creature */}
                <div className="col-start-2 row-start-1 flex justify-center items-center">
                    <div className="relative">
                        <div className="w-32 h-32 bg-gray-400 rounded-full opacity-20 absolute bottom-0" />
                        <Card className="w-32 h-32 flex items-center justify-center">
                            {opponent_creature?.display_name || 'No Creature'}
                        </Card>
                    </div>
                </div>

                {/* Player Creature */}
                <div className="col-start-1 row-start-2 flex justify-center items-center">
                    <div className="relative">
                        <div className="w-32 h-32 bg-gray-400 rounded-full opacity-20 absolute bottom-0" />
                        <Card className="w-32 h-32 flex items-center justify-center">
                            {player_creature?.display_name || 'No Creature'}
                        </Card>
                    </div>
                </div>

                {/* Player Stats */}
                <div className="col-start-2 row-start-2">
                    {player_creature && (
                        <CreatureStats 
                            creature={player_creature} 
                            uid={player_creature.uid}
                        />
                    )}
                </div>
            </div>

            {/* UI Area */}
            <Card className="flex-grow-1 p-4 rounded-none bg-slate-800">
                <div className="grid grid-cols-2 gap-4">
                    {player_creature?.collections.skills.map((skill) => (
                        availableButtonSlugs.includes(skill.meta.prototype_id) && (
                            <Button
                                key={skill.uid}
                                onClick={() => emitButtonClick(skill.meta.prototype_id)}
                                variant="secondary"
                                className="h-auto flex flex-col items-start p-4"
                            >
                                <div className="font-bold">{skill.display_name}</div>
                                <div className="text-sm opacity-80">{skill.description}</div>
                            </Button>
                        )
                    ))}
                </div>
            </Card>
        </div>
    );
}
