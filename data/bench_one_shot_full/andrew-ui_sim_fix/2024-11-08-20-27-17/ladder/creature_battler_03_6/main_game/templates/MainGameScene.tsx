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
        skill_type: string;
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
    meta: {
        creature_type: string;
    };
    collections: {
        skills: Skill[];
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
    } = useCurrentButtons()

    const playerCreature = props.data?.entities?.player_creature
    const opponentCreature = props.data?.entities?.opponent_creature

    if (!playerCreature || !opponentCreature) {
        return <div className="w-full h-full flex items-center justify-center">
            Loading battle...
        </div>
    }

    const renderHealthBar = (current: number, max: number) => (
        <div className="w-full h-2 bg-gray-200 rounded-full" role="progressbar" 
             aria-valuemin={0} aria-valuemax={max} aria-valuenow={current}>
            <div 
                className="h-full bg-green-500 rounded-full transition-all duration-300"
                style={{ width: `${(current / max) * 100}%` }}
            />
        </div>
    )

    const renderCreatureStats = (creature: Creature) => (
        <div className="flex gap-2 text-sm">
            <span className="flex items-center gap-1" aria-label="Health">
                <Heart className="w-4 h-4" /> {creature.stats.hp}/{creature.stats.max_hp}
            </span>
            <span className="flex items-center gap-1" aria-label="Attack">
                <Sword className="w-4 h-4" /> {creature.stats.attack}
            </span>
            <span className="flex items-center gap-1" aria-label="Defense">
                <Shield className="w-4 h-4" /> {creature.stats.defense}
            </span>
            <span className="flex items-center gap-1" aria-label="Speed">
                <Zap className="w-4 h-4" /> {creature.stats.speed}
            </span>
        </div>
    )

    return (
        <div className="w-full h-full flex flex-col">
            <nav className="h-[10%] bg-gray-800 text-white px-4 flex items-center" 
                 role="navigation" aria-label="Battle status">
                Battle in Progress
            </nav>

            <div className="h-[50%] flex items-center justify-between px-8 bg-gray-100" 
                 role="region" aria-label="Battlefield">
                <Card className="w-1/3 p-4">
                    <div className="space-y-2">
                        <h3 className="text-xl font-bold">{playerCreature.display_name}</h3>
                        {renderHealthBar(playerCreature.stats.hp, playerCreature.stats.max_hp)}
                        {renderCreatureStats(playerCreature)}
                        <span className="text-sm text-blue-500">
                            {playerCreature.meta.creature_type} type
                        </span>
                    </div>
                </Card>

                <Card className="w-1/3 p-4">
                    <div className="space-y-2">
                        <h3 className="text-xl font-bold">{opponentCreature.display_name}</h3>
                        {renderHealthBar(opponentCreature.stats.hp, opponentCreature.stats.max_hp)}
                        {renderCreatureStats(opponentCreature)}
                        <span className="text-sm text-red-500">
                            {opponentCreature.meta.creature_type} type
                        </span>
                    </div>
                </Card>
            </div>

            <div className="h-[40%] bg-white p-4 border-t-2" role="region" aria-label="Battle controls">
                <div className="grid grid-cols-2 gap-4">
                    {playerCreature.collections?.skills?.map(skill => (
                        availableButtonSlugs.includes(skill.uid) && (
                            <Button
                                key={skill.uid}
                                onClick={() => emitButtonClick(skill.uid)}
                                variant="default"
                                className="h-auto flex flex-col items-start p-4 space-y-1"
                                aria-label={`Use ${skill.display_name}`}
                            >
                                <span className="font-bold">{skill.display_name}</span>
                                <span className="text-sm">{skill.description}</span>
                                <span className="text-xs">
                                    Base Damage: {skill.stats.base_damage}
                                </span>
                            </Button>
                        )
                    ))}
                </div>
            </div>
        </div>
    )
}
