import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
  hp: number
  maxHp: number
}

interface CardComponentProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let CustomCard = React.forwardRef<HTMLDivElement, CardComponentProps>(
  ({ uid, ...props }, ref) => <Card ref={ref} {...props} />
)

let CustomCardHeader = React.forwardRef<HTMLDivElement, CardComponentProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let CustomCardContent = React.forwardRef<HTMLDivElement, CardComponentProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

let CustomCardTitle = React.forwardRef<HTMLParagraphElement, CardComponentProps & React.HTMLAttributes<HTMLHeadingElement>>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

CustomCard = withClickable(CustomCard)
CustomCardHeader = withClickable(CustomCardHeader)
CustomCardContent = withClickable(CustomCardContent)
CustomCardTitle = withClickable(CustomCardTitle)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, imageUrl, hp, maxHp, ...props }, ref) => {
    return (
      <CustomCard uid={`${uid}-card`} ref={ref} className={cn("w-[350px]", className)} {...props}>
        <CustomCardHeader uid={`${uid}-header`}>
          <CustomCardTitle uid={`${uid}-title`}>{name}</CustomCardTitle>
        </CustomCardHeader>
        <CustomCardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img 
              src={imageUrl}
              alt={name}
              className="w-full h-48 object-contain"
            />
            <div className="w-full bg-secondary h-2 rounded-full">
              <div 
                className="bg-primary h-2 rounded-full transition-all"
                style={{ width: `${(hp / maxHp) * 100}%` }}
              />
            </div>
            <div className="text-sm text-right">
              {hp}/{maxHp} HP
            </div>
          </div>
        </CustomCardContent>
      </CustomCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard, CustomCard, CustomCardHeader, CustomCardContent, CustomCardTitle }
