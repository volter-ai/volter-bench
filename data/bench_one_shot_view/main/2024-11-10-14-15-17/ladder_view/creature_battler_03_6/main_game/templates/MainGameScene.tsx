import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap, Heart } from 'lucide-react';

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
        skills: Array<{
            uid: string;
            display_name: string;
            description: string;
            meta: {
                prototype_id: string;
            };
            stats: {
                base_damage: number;
            };
        }>;
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
        return <div className="w-full aspect-video flex items-center justify-center">
            Loading battle...
        </div>;
    }

    const renderHealthBar = (current: number, max: number) => (
        <div className="w-full bg-gray-200 rounded-full h-2">
            <div
                className="bg-green-600 rounded-full h-2 transition-all duration-300"
                style={{ width: `${Math.max(0, Math.min(100, (current / max) * 100))}%` }}
            />
        </div>
    );

    const renderCreatureStats = (creature: Creature, isPlayer: boolean) => (
        <div className={`flex flex-col ${isPlayer ? 'items-start' : 'items-end'} p-4 bg-white/10 rounded-lg`}>
            <h2 className="text-xl font-bold">{creature.display_name}</h2>
            <div className="w-48">
                {renderHealthBar(creature.stats.hp, creature.stats.max_hp)}
            </div>
            <div className="flex gap-2 mt-2 text-sm">
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
    );

    return (
        <div className="w-full aspect-video bg-gradient-to-b from-blue-900 to-blue-800 text-white flex flex-col">
            {/* HUD */}
            <nav className="h-[10%] bg-black/30 p-4">
                <div className="flex justify-between items-center">
                    <div className="flex items-center gap-2">
                        <Heart className="text-red-500" />
                        Battle Scene
                    </div>
                </div>
            </nav>

            {/* Battlefield */}
            <div className="h-[50%] flex justify-between items-center px-8">
                <div className="relative">
                    {renderCreatureStats(playerCreature, true)}
                    <span className="absolute -top-6 left-0 text-sm">Player</span>
                </div>
                <div className="relative">
                    {renderCreatureStats(opponentCreature, false)}
                    <span className="absolute -top-6 right-0 text-sm">Opponent</span>
                </div>
            </div>

            {/* UI Region */}
            <div className="h-[40%] bg-black/40 p-4 rounded-t-xl">
                <div className="grid grid-cols-2 gap-4">
                    {playerCreature.collections?.skills?.map((skill) => {
                        const skillId = skill.meta.prototype_id;
                        if (!availableButtonSlugs.includes(skillId)) return null;
                        
                        return (
                            <button
                                key={skillId}
                                onClick={() => emitButtonClick(skillId)}
                                className="p-4 bg-blue-600 hover:bg-blue-700 rounded-lg text-left transition-colors"
                            >
                                <h3 className="font-bold">{skill.display_name}</h3>
                                <p className="text-sm opacity-80">{skill.description}</p>
                                <span className="text-xs mt-1 opacity-60">
                                    Damage: {skill.stats.base_damage}
                                </span>
                            </button>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
