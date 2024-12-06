import * as React from "react"
import { cn } from "@/lib/utils"
import { 
  Card as ShadcnCard, 
  CardContent as ShadcnCardContent, 
  CardHeader as ShadcnCardHeader, 
  CardTitle as ShadcnCardTitle 
} from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface BaseProps {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentPropsWithoutRef<typeof ShadcnCard>>(
  ({ uid, ...props }, ref) => <ShadcnCard {...props} ref={ref} />
)

let CardHeader = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentPropsWithoutRef<typeof ShadcnCardHeader>>(
  ({ uid, ...props }, ref) => <ShadcnCardHeader {...props} ref={ref} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, BaseProps & React.ComponentPropsWithoutRef<typeof ShadcnCardTitle>>(
  ({ uid, ...props }, ref) => <ShadcnCardTitle {...props} ref={ref} />
)

let CardContent = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentPropsWithoutRef<typeof ShadcnCardContent>>(
  ({ uid, ...props }, ref) => <ShadcnCardContent {...props} ref={ref} />
)

Card = withClickable(Card)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)
CardContent = withClickable(CardContent)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
          <div className="h-4 w-full bg-gray-200 rounded-full">
            <div 
              className="h-4 bg-green-500 rounded-full" 
              style={{width: `${(hp/maxHp) * 100}%`}}
            />
          </div>
          <div className="text-sm text-right">
            {hp}/{maxHp} HP
          </div>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <img 
            src={imageUrl}
            alt={name}
            className="w-full h-48 object-contain"
          />
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
